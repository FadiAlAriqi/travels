import frappe
from frappe.utils import nowdate, nowtime, get_datetime
from frappe.model.mapper import get_mapped_doc
from frappe import _

@frappe.whitelist()
def make_payment_entry(source_name, target_doc=None):
    def update_item(source, target, source_parent):
        target.party_type = "Customer"
        target.party = source.customer_name
        target.party_name = source.customer_name
        # target.paid_to = source.shipper_name
        # target.paid_from = source.debit_to
        target.payment_type = "Receive"
        # target.custom_total_amount =source.outstanding
        # account_currency = frappe.db.get_value("Account", source.debit_to, "account_currency")
        # target.paid_from_account_currency = account_currency
        target.receved_amount = source.total


    doc = get_mapped_doc(
        "Booking Services",  
        source_name,
        {
            "Booking Services": {
                "doctype": "Payment Entry",
                "field_map": {
                    "customer": "party",
                    "total": "paid_amount",
                    
                },
                "postprocess": update_item,
            },
        },
        target_doc
    )

    return doc

# @frappe.whitelist()
# def make_payment_entry_from_hotel(source_name):
    # def update_item(source, target, source_parent):
    #     # تعيين الحقول الرئيسية
    #     target.party_type = "Supplier"
    #     target.payment_type = "Pay"
        
    #     # المرور على الحقول داخل التشايلد تيبل (hotel)
    #     if source.hotel:
    #         for hotel_entry in source.hotel:
    #             # التأكد من وجود القيم المطلوبة
    #             if hotel_entry.hotel_name and hotel_entry.hotel_payable_amount:
    #                 frappe.msgprint(f"Processing Hotel: {hotel_entry.hotel_name} with Amount: {hotel_entry.hotel_payable_amount}")
    #                 target.party = "Al-Ola"
    #                 target.paid_amount = 200
    #             else:
    #                 frappe.msgprint("Missing data in hotel entry")

    # try:
    #     # إنشاء المستند الجديد مع تنفيذ postprocess
    #     doc = get_mapped_doc(
    #         "Booking Services",  # اسم الدوكيومنت سورس
    #         source_name,  # اسم السجل في Booking Services
    #         {
    #             "Booking Services": {
    #                 "doctype": "Payment Entry",  # المستند المستهدف
    #                 "postprocess": update_item,  # معالجة التحديث
    #             },
    #         }
    #     )
        
    #     frappe.msgprint(f"Payment Entry created successfully: {doc.name}")
    

    # except Exception as e:
    #     # تسجيل أي خطأ يحدث أثناء التنفيذ
    #     frappe.log_error(f"Error: {str(e)}", "Payment Entry Creation Error")
    #     frappe.throw(_("An error occurred while creating the Payment Entry."))


@frappe.whitelist()
def make_payment_entry_from_hotel(source_name):
    def update_item(source, target, source_parent):
        target.party_type = "Supplier"
        target.party = source.hotel
        target.custom_supplier = source.hotel
        target.party_name = source.hotel
        target.payment_type = "Pay"
        target.paid_amount = source.hotel_amount
        target.received_amount = source.hotel_amount
    # استدعاء get_mapped_doc مع الخريطة الصحيحة
    doc = get_mapped_doc(
        "Hotel Booking",  # اسم المصدر
        source_name,      # اسم السجل المصدر
        {
            "Hotel Booking": {  # تعريف DocType المصدر
                "doctype": "Payment Entry",  # اسم DocType الهدف
                "field_map": {  # خريطة الحقول
                    "supplier": "party",
                    "hotel_amount": "paid_amount",
                },
                "postprocess": update_item,  # دالة التحديث بعد المعالجة
            },
        }
    )

    return doc




# @frappe.whitelist()
# def make_payment_entry_from_hotel(source_name):
#     def update_item(source, target, source_parent):
#         target.party_type = "Supplier"
        
#         # استعراض التشابلد تيبل (hotel) واستخدام البيانات منه
#         for hotel_entry in source.hotel:  # استعراض البيانات داخل الـ hotel child table
#             target.party = hotel_entry.hotel_name  # استخدام اسم الفندق من الـ child table
#             target.party_name = hotel_entry.hotel_name
#             target.payment_type = "Pay"
#             target.paid_amount = hotel_entry.hotel_payable_amount  # إذا كان هناك حقل للمدفوعات في التشابلد تيبل

#     try:
#         # الحصول على البيانات من Booking Services ونسخها إلى Payment Entry
#         doc = get_mapped_doc(
#             "Booking Services",  # اسم الـ DocType الأصلي
#             source_name,
#             {
#                 "Booking Services": {
#                     "doctype": "Payment Entry",  # الـ DocType الهدف
#                     "field_map": {
#                         "customer": "party",  # مثال: ربط حقل العميل بالـ party في Payment Entry
#                         "hotel_payable_amount": "paid_amount",  # ربط حقل المبلغ المدفوع
#                     },
#                     "postprocess": update_item,  # معالجة البيانات بعد النقل
#                 },
#             },
#             target_doc=None  # لا حاجة لتحديد هدف إذا كنت ستقوم بإنشاء الـ doc مباشرة
#         )
#         return doc  # إرجاع الـ Payment Entry المنشأ

#     except Exception as e:
#         frappe.log_error(f"Error while creating payment entry: {str(e)}", "Make Payment Entry Error")


# @frappe.whitelist()
# def make_payment_entry_from_hotel(source_name, target_doc=None):
#     def update_item(source, target, source_parent):
#         # تعيين القيم المطلوبة في مستند Payment Entry
#         target.party_type = "Supplier"  # نوع الطرف
#         target.party = source.hotel  # اسم الفندق كطرف
#         target.party_name = source.hotel  # اسم المورد
#         target.payment_type = "Pay"  # نوع الدفع
#         target.paid_amount = source.hotel_amount  # المبلغ المدفوع
#         target.received_amount = 0  # المبلغ المستلم (صفر افتراضيًا)
    
#     # استخدام الدالة get_mapped_doc لإنشاء مستند جديد
#     doc = get_mapped_doc(
#         "Hotel Booking",  # اسم المستند المصدر
#         source_name,  # اسم السجل المصدر
#         {
#             "Hotel Booking": {  # إعدادات الماب
#                 "doctype": "Payment Entry",  # اسم المستند الهدف
#                 "field_map": {  # خريطة الحقول
#                     "hotel": "party",  # ربط حقل الفندق مع الطرف
#                     "hotel_amount": "paid_amount",  # ربط حقل المبلغ المدفوع
#                 },
#                 "postprocess": update_item,  # تنفيذ المعالجة بعد النقل
#             },
#         },
#         target_doc
#     )

#     return doc


@frappe.whitelist()
def make_payment_entry_from_transport_company(source_name, target_doc=None):
    def update_item(source, target, source_parent):
        # تعيين القيم المطلوبة في مستند Payment Entry
        target.party_type = "Supplier"  # نوع الطرف
        target.party = source.company  # اسم الفندق كطرف
        target.party_name = source.company  # اسم المورد
        target.payment_type = "Pay"  # نوع الدفع
        target.paid_amount = source.rental_company_amount  # المبلغ المدفوع
        # target.received_amount = 0  # المبلغ المستلم (صفر افتراضيًا)
    
    # استخدام الدالة get_mapped_doc لإنشاء مستند جديد
    doc = get_mapped_doc(
        "Vehicle Rental",  # اسم المستند المصدر
        source_name,  # اسم السجل المصدر
        {
            "Vehicle Rental": {  # إعدادات الماب
                "doctype": "Payment Entry",  # اسم المستند الهدف
                "field_map": {  # خريطة الحقول
                    "company": "party",  # ربط حقل الفندق مع الطرف
                    "rental_company_amount": "paid_amount",  # ربط حقل المبلغ المدفوع
                },
                "postprocess": update_item,  # تنفيذ المعالجة بعد النقل
            },
        },
        target_doc
    )

    return doc

@frappe.whitelist()
def make_payment_entry_from_ticket(source_name):
    def update_item(source, target, source_parent):
        target.party_type = "Supplier"
        target.party = source.airline
        target.party_name = source.airline
        target.payment_type = "Pay"
        target.paid_amount = source.total_amount
        target.received_amount = source.total_amount
    # استدعاء get_mapped_doc مع الخريطة الصحيحة
    doc = get_mapped_doc(
        "Ticket Booking",  # اسم المصدر
        source_name,      # اسم السجل المصدر
        {
            "Ticket Booking": {  # تعريف DocType المصدر
                "doctype": "Payment Entry",  # اسم DocType الهدف
                "field_map": {  # خريطة الحقول
                    "supplier": "party",
                    "total_amount": "paid_amount",
                },
                "postprocess": update_item,  # دالة التحديث بعد المعالجة
            },
        }
    )

    return doc

#    update_booking_status depending on departure_date   departure_time
@frappe.whitelist() 
def update_booking_status():
    # الحصول على كل التذاكر التي لم تكتمل بعد
    tickets = frappe.get_all('Ticket Booking', filters={'booking_status': 'Booked'}, fields=['name', 'departure_date', 'departure_time'])
    
    frappe.log_error(f"Error while fadi eating:", "Hi Esmail")

    for ticket in tickets:
        departure_datetime = get_datetime(f"{ticket['departure_date']} {ticket['departure_time']}")
        current_datetime = get_datetime(f"{nowdate()} {nowtime()}")

        if current_datetime > departure_datetime:
            # تحديث الحالة إلى Completed إذا كان الوقت الحالي أكبر من وقت الرحلة
            frappe.db.set_value('Ticket Booking', ticket['name'], 'booking_status', 'Completed')
            frappe.db.commit()
            frappe.msgprint(f"Booking {ticket['name']} status updated to Completed")
