import frappe
from frappe.utils import nowdate, nowtime, get_datetime
from frappe.model.mapper import get_mapped_doc
from frappe import _
import requests
from frappe.utils import now
import json


@frappe.whitelist()
def make_payment_entry(source_name, target_doc=None):
    def update_item(source, target, source_parent):
        target.party_type = "Customer"
        target.party = source.customer_name
        target.party_name = source.customer_name
        target.payment_type = "Receive"
        target.received_amount = source.outstanding
        target.custom_total_amount = source.outstanding



    doc = get_mapped_doc(
        "Booking Services",  
        source_name,
        {
            "Booking Services": {
                "doctype": "Payment Entry",
                "field_map": {
                    "customer": "party",
                    "outstanding": "paid_amount",
                    
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
        target.custom_total_amount = source.hotel_amount

    doc = get_mapped_doc(
        "Hotel Booking",  
        source_name,      
        {
            "Hotel Booking": {  
                "doctype": "Payment Entry", 
                "field_map": {  
                    "supplier": "party",
                    "hotel_amount": "paid_amount",
                },
                "postprocess": update_item,  
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
        target.party_type = "Supplier"
        target.party = source.company  
        target.party_name = source.company  
        target.payment_type = "Pay" 
        target.paid_amount = source.rental_company_amount  
        target.custom_total_amount = source.rental_company_amount  

    
    doc = get_mapped_doc(
        "Vehicle Rental",  
        source_name,  
        {
            "Vehicle Rental": {  
                "doctype": "Payment Entry",  
                "field_map": {  
                    "company": "party",  
                    "rental_company_amount": "paid_amount", 
                },
                "postprocess": update_item, 
            },
        },
        target_doc
    )

    return doc

@frappe.whitelist()
def make_payment_entry_from_ticket(source_name):ؤي
    def update_item(source, target, source_parent):
        target.party_type = "Supplier"
        target.party = source.airline
        target.party_name = source.airline
        target.payment_type = "Pay"
        target.paid_amount = source.total_amount
        target.received_amount = source.total_amount
        target.custom_total_amount = source.total_amount

    doc = get_mapped_doc(
        "Ticket Booking",  
        source_name,      
        {
            "Ticket Booking": {  
                "doctype": "Payment Entry",  
                "field_map": {  
                    "supplier": "party",
                    "total_amount": "paid_amount",
                },
                "postprocess": update_item,  
            },
        }
    )

    return doc

#    update_booking_status depending on departure_date   departure_time
@frappe.whitelist() 
def update_booking_status():
    tickets = frappe.get_all('Ticket Booking', filters={'booking_status': 'Booked'}, fields=['name', 'departure_date', 'departure_time'])
    
    for ticket in tickets:
        departure_datetime = get_datetime(f"{ticket['departure_date']} {ticket['departure_time']}")
        current_datetime = get_datetime(f"{nowdate()} {nowtime()}")

        if current_datetime > departure_datetime:
            frappe.db.set_value('Ticket Booking', ticket['name'], 'booking_status', 'Completed')
            frappe.db.commit()
            frappe.msgprint(f"Booking {ticket['name']} status updated to Completed")




@frappe.whitelist() 
def fetch_and_store_flight_offers():
    url = "https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=SYD&destinationLocationCode=BKK&departureDate=2025-05-02&adults=1&nonStop=false&max=250"

    headers = {
        "Authorization": "Bearer azaB4rvQXHqfwC3ShIEZo3AG1CHv"  }
    # frappe.msgprint("hiiii")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for offer in data.get("data", []):
            flight_offer = frappe.get_doc({
                "doctype": "Flight Offer",
                "type": offer.get("type"),
                "name": offer.get("id"),
                "source": offer.get("source"),
                "instant_ticketing_required": offer.get("instantTicketingRequired"),
                "last_ticketing_date": offer.get("lastTicketingDate"),
                "number_of_bookable_seats": offer.get("numberOfBookableSeats"),
                "price_currency": offer["price"].get("currency"),
                "price_total": offer["price"].get("total"),
                "offer_details": json.dumps(offer),  
            })

            flight_offer.insert()
            frappe.db.commit()
    else:
        frappe.throw(f"Failed to fetch data from API: {response.status_code}")

# Amadeus Hotels
@frappe.whitelist()
def fetch_and_store_hotels():
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode=PAR&radius=5&radiusUnit=KM&amenities=AIR_CONDITIONING&ratings=5&hotelSource=ALL"  # استبدل بالرابط الصحيح لـ API الخاص بك

    headers = {
        "Authorization": "Bearer VaayN3xVqYpno5K57DMOktZJIJeC" 
    }
    # frappe.msgprint("hiiii")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for hotel in data.get("data", []):
            if not frappe.db.exists("Amadeus Hotels", {"hotelid": hotel.get("hotelId")}):
                hotel_doc = frappe.get_doc({
                    "doctype": "Amadeus Hotels",
                    "name1": hotel.get("name"),
                    "chaincode": hotel.get("chainCode"),
                    "iatacode": hotel.get("iataCode"),
                    "dupeid": hotel.get("dupeId"),
                    "hotelid": hotel.get("hotelId"),
                    "countrycode": hotel["address"].get("countryCode"),
                    "rating": hotel.get("rating"),
                    "lastupdate": hotel.get("lastUpdate"),
                })

                for amenity in hotel.get("amenities", []):
                    hotel_doc.append("amenities", {
                        "amenity": amenity
                    })

                distance = hotel.get("distance", {})
                if distance:
                    hotel_doc.append("distance", {
                        "value": distance.get("value"),
                        "unit": distance.get("unit")
                    })

                hotel_doc.insert()
                frappe.db.commit()

    else:
        frappe.throw(f"Failed to fetch data from API: {response.status_code}")

# Standard  Hotels
@frappe.whitelist()
def fetch_and_store_hotels2():
    url = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city?cityCode=PAR&radius=5&radiusUnit=KM&hotelSource=ALL"  # استبدل بالرابط الصحيح لـ API الخاص بك

    headers = {
        "Authorization": "Bearer 8TYr6fn6OkBmsaLqA8rw12YuGA3L" 
    }
    frappe.msgprint("hiiii")
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        for hotel in data.get("data", []):
            if not frappe.db.exists("Hotel", {"hotelid": hotel.get("hotelId")}):
                hotel_doc = frappe.get_doc({
                    "doctype": "Hotel",
                    "hotel_name": hotel.get("name"),
                    "type": "Hotel",
                    "chaincode": hotel.get("chainCode"),
                    "city": hotel.get("iataCode"),
                    # "dupeid": hotel.get("dupeId"),
                    # "hotelid": hotel.get("hotelId"),
                    "country": hotel["address"].get("countryCode"),
                    "category": hotel.get("rating"),
                    # "lastupdate": hotel.get("lastUpdate"),
                })

                # for amenity in hotel.get("amenities", []):
                #     hotel_doc.append("amenities", {
                #         "amenity": amenity
                #     })

                # distance = hotel.get("distance", {})
                # if distance:
                #     hotel_doc.append("distance", {
                #         "value": distance.get("value"),
                #         "unit": distance.get("unit")
                #     })

                hotel_doc.insert()
                frappe.db.commit()

    else:
        frappe.throw(f"Failed to fetch data from API: {response.status_code}")