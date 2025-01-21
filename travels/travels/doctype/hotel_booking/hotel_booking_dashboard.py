from frappe import _

def get_data(data=None):
    return {
        "fieldname": "custom_reference_hotel",  # الحقل المستخدم للربط
        "transactions": [
            {
                "label": _("Create Payments"),
                "items": ["Payment Entry"],  # المستند المرتبط
                "method": "travels.travels.doctype.hotel_booking.hotel_booking.make_payment_entry" 
            },
        ],
    }
