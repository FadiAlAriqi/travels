from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
import frappe
from frappe.model.mapper import get_mapped_doc
from frappe.utils import fmt_money
from frappe import _
from frappe.model.document import Document

# class MyCustomPaymentEntry(PaymentEntry):  # تغيير الوراثة من PaymentEntry إلى EmployeePaymentEntry
#     def on_submit(self):
#         frappe.msgprint("Custom Payment Entry Triggered")
#         super().on_submit()

#         booking_service_name = self.custom_booking_service

#         if booking_service_name:
#             total_amount = float(self.custom_total_amount or 0.0)
#             paid_amount = float(self.paid_amount or 0.0)
#             payment_type = self.payment_type

#             updated_outstanding = total_amount - paid_amount

#             if payment_type == "Receive":
#                 frappe.db.set_value("Booking Service", booking_service_name, "outstanding", updated_outstanding)

#             frappe.db.commit()

#             booking_service_doc = frappe.get_doc("Booking Service", booking_service_name)
#             booking_service_doc.reload()
#             booking_service_doc.save()
            
#     def validate(self):
#         paid_amount = self.paid_amount or 0.0
#         custom_total_amount = self.custom_total_amount or 0.0

#         # منع إدخال paid_amount أكبر من custom_total_amount
#         if paid_amount > custom_total_amount:
#             frappe.throw(_("The paid amount cannot be greater than the total amount."))


def update_outstanding(doc, method):
    booking_service_name = doc.custom_booking_service
    hotel_booking_name = doc.custom_hotel_
    vehicle_rental_name=doc.custom_vehicle
    ticket_name=doc.custom_ticket


    if booking_service_name:
        total_amount = float(doc.custom_total_amount or 0.0)
        paid_amount = float(doc.paid_amount or 0.0)
        payment_type = doc.payment_type

        updated_outstanding = total_amount - paid_amount

        if payment_type == "Receive":
            
            frappe.db.set_value("Booking Services", booking_service_name, "outstanding", updated_outstanding)

            # تحديث حالة الحجز
            new_status = "Paid" if updated_outstanding == 0 else "Partially Paid" if updated_outstanding < total_amount else "Unpaid"
            frappe.db.set_value("Booking Services", booking_service_name, "status", new_status)

            frappe.db.commit()

            # إعادة تحميل المستند بعد التحديث
            booking_service_doc = frappe.get_doc("Booking Services", booking_service_name)
            booking_service_doc.reload()

    elif hotel_booking_name:
            new_status = "Paid"  
            frappe.db.set_value("Hotel Booking", hotel_booking_name, "status", new_status)
            hotel_booking_doc = frappe.get_doc("Hotel Booking", hotel_booking_name)
            hotel_booking_doc.reload()
    elif vehicle_rental_name:
            new_status = "Paid"  
            frappe.db.set_value("Vehicle Rental", vehicle_rental_name, "status", new_status)
            vehicle_rental_doc = frappe.get_doc("Vehicle Rental", vehicle_rental_name)
            vehicle_rental_doc.reload() 
    elif ticket_name:
            
        new_status = "Paid"  
        frappe.db.set_value("Ticket Booking", ticket_name, "status", new_status)
        ticket_booking_doc = frappe.get_doc("Ticket Booking", ticket_name)
        ticket_booking_doc.reload() 

frappe.db.commit()



def validate_amounts(doc, method):
    total_amount = float(doc.custom_total_amount or 0.0)
    paid_amount = float(doc.paid_amount or 0.0)
    payment_type = doc.payment_type

    if total_amount <= 0:
        frappe.throw(_("Total amount must be greater than zero."))

    if paid_amount < 0:
        frappe.throw(_("Paid amount cannot be negative."))

    if payment_type == "Receive":
        if paid_amount > total_amount:
            frappe.throw(_(f"Paid Amount Can Not Be Greater Than Total Amount"))
    else:
         if paid_amount!= total_amount:
            frappe.throw(_(f"Paid Amount Can Not Be Less Than Total Amount"))
 
