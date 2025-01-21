# Copyright (c) 2025, Yemen Frappe and contributors
# For license information, please see license.txt
from erpnext.controllers.accounts_controller import AccountsController
from erpnext.accounts.general_ledger import make_gl_entries
from frappe import _

import frappe 
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
	get_accounting_dimensions,
	get_dimensions,
)
import erpnext
import traceback
from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import (
    get_accounting_dimensions,
)
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
from frappe.model.meta import get_meta


from erpnext.accounts.utils import  get_account_currency
from erpnext.assets.doctype.asset.depreciation import (
	depreciate_asset,
	get_disposal_account_and_cost_center,
	get_gl_entries_on_asset_disposal,
	get_gl_entries_on_asset_regain,
	reset_depreciation_schedule,
	reverse_depreciation_entry_made_after_disposal,
)

from frappe import _, qb, throw
from frappe.model.mapper import get_mapped_doc
from frappe.query_builder.functions import Sum
from frappe.utils import cint, cstr, flt, formatdate, get_link_to_form, getdate, nowdate

import erpnext
from erpnext.accounts.deferred_revenue import validate_service_stop_date
from erpnext.accounts.doctype.gl_entry.gl_entry import update_outstanding_amt
from erpnext.accounts.doctype.repost_accounting_ledger.repost_accounting_ledger import (
	validate_docs_for_deferred_accounting,
	validate_docs_for_voucher_types,
)
from erpnext.accounts.doctype.sales_invoice.sales_invoice import (
	check_if_return_invoice_linked_with_payment_entry,
	get_total_in_party_account_currency,
	is_overdue,
	unlink_inter_company_doc,
	update_linked_doc,
	validate_inter_company_party,
)
from erpnext.accounts.doctype.tax_withholding_category.tax_withholding_category import (
	get_party_tax_withholding_details,
)
from erpnext.accounts.general_ledger import (
	get_round_off_account_and_cost_center,
	make_gl_entries,
	make_reverse_gl_entries,
	merge_similar_entries,
)
from erpnext.accounts.party import get_due_date, get_party_account
from erpnext.accounts.utils import get_account_currency, get_fiscal_year
from erpnext.assets.doctype.asset.asset import is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.controllers.accounts_controller import validate_account_head
from erpnext.controllers.buying_controller import BuyingController
from erpnext.stock import get_warehouse_account_map
from erpnext.stock.doctype.purchase_receipt.purchase_receipt import (
	get_item_account_wise_additional_cost,
	update_billed_amount_based_on_po,
)
from erpnext.assets.doctype.asset_activity.asset_activity import add_asset_activity
from erpnext.accounts.general_ledger import (
    make_gl_entries,
    merge_similar_entries,
)
from erpnext.accounts.party import get_party_account


from erpnext.accounts.general_ledger import (
	make_gl_entries,
	make_reverse_gl_entries,
	process_gl_map,
)
from erpnext.accounts.utils import (
	create_gain_loss_journal,
	get_account_currency,
	get_currency_precision,
	get_fiscal_years,
	validate_fiscal_year,
)
from frappe.utils import cint, comma_or, flt, getdate, nowdate
from erpnext.accounts.utils import (
	cancel_exchange_gain_loss_journal,
	get_account_currency,
	get_balance_on,
	get_outstanding_invoices,
	get_party_types_from_account_type,
)
from erpnext.accounts.party import get_party_account

from erpnext.accounts.doctype.bank_account.bank_account import (
	get_bank_account_details,
	# get_default_company_bank_account,
	get_party_bank_account,
)
from erpnext.accounts.doctype.invoice_discounting.invoice_discounting import (
	get_party_account_based_on_invoice_discounting,
)
from erpnext.controllers.accounts_controller import AccountsController

class BookingServices(AccountsController):
    def on_submit(self):
        # التأكد من الحقول الأساسية
        if not self.total or self.total <= 0:
            frappe.throw(_("Total amount must be greater than zero."))
        
        if not self.debit_to:
            frappe.throw(_("Please select a valid Debit To account (Debtor account)."))
        
        if not self.income_account:
            frappe.throw(_("Please select a valid Income account."))
        
        # إنشاء القيود المحاسبية
        self.make_gl_entries()


    def make_gl_entries(self):
        # إعداد قيود الحسابات المدينة (debit)
        gl_entries = [
            self.get_gl_dict({
                "account": self.debit_to,  # حساب العميل المدين
                "debit": flt(self.total),  # المبلغ المدين
                "credit": 0,  # دائنة صفر
                "posting_date": frappe.utils.today(),  # تاريخ القيد
                "against": self.income_account,  # الحساب المقابل
                "party_type": "Customer",
                "party": self.customer_name,  # اسم العميل
                "company": self.company,
            }),
            self.get_gl_dict({
                "account": self.income_account,  # حساب الإيرادات الدائن
                "debit": 0,  # مدينة صفر
                "credit": flt(self.total),  # المبلغ الدائن
                "posting_date":frappe.utils.today(),  # تاريخ القيد
                "against": self.debit_to,  # الحساب المقابل
                "company": self.company,
            })
        ]

        # إرسال القيود إلى الدالة المسؤولة عن إدخالها
        make_gl_entries(gl_entries)

    def get_gl_dict(self, args):
        """إنشاء قاموس القيد المحاسبي"""
        gl_dict = frappe._dict({
            "company": self.company,
            "posting_date":frappe.utils.today(),
            "voucher_type": self.doctype,
            "voucher_no": self.name,
            "remarks": getattr(self, "remarks", _("Accrual entry for booking services")),
            "debit": 0,
            "credit": 0,
            "is_opening": "No",
        })
        gl_dict.update(args)
        return gl_dict

    def validate(self):
        # استدعاء دالة حساب المجموع عند الحفظ
        self.calculate_total_tickets_amount()
        self.calculate_total_hotels_amount()
        self.calculate_total_rental_vehicles_amount()


#calculate total price for all tickets
    def calculate_total_tickets_amount(self):
        total_tickets_amount = sum(ticket.total_ticket_amount for ticket in self.ticket if ticket.total_ticket_amount)
        
        self.total_tickets_amount = total_tickets_amount

#calculate total price for all hotels

    def calculate_total_hotels_amount(self):
        total_hotels_amount = sum(hotel.booking_amount for hotel in self.hotel if hotel.booking_amount)

        self.total_hotels_amount = total_hotels_amount


#calculate total price for all rental vehicles

    def calculate_total_rental_vehicles_amount(self):
        total_rental_vehicles_amount = sum(vehicle.booking_amount for vehicle in self.vehicle if vehicle.booking_amount)

        self.total_rental_vehicles_amount = total_rental_vehicles_amount
