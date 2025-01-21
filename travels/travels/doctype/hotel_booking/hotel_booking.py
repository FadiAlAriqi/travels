# Copyright (c) 2025, YemenFrappe and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class HotelBooking(Document):
	@frappe.whitelist()
	def make_payment_entry(source_name, target_doc=None):
		frappe.msgprint("hi")
		def set_missing_values(source, target):
			target.payment_type = 'Pay'  # ضبط نوع الدفع إلى "Pay"
			target.custom_reference_hotel = source.name  # ربط المستند بالحجز الحالي
			# يمكنك إضافة المزيد من الحقول هنا
			target.posting_date = frappe.utils.nowdate()

		doc = get_mapped_doc(
			"Hotel Booking",
			source_name,
			{
				"Hotel Booking": {
					"doctype": "Payment Entry",
					"field_map": {
						"name": "custom_reference_hotel",  # ربط الحقول
					},
				}
			},
			target_doc,
			set_missing_values,
		)

		return doc
