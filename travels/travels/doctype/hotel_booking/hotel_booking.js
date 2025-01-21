// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Hotel Booking', {
//     price_per_night: function(frm) {
//         if (frm.doc.price_per_night && frm.doc.commission_rate) {
//             // Calculate commission_amount and amount
//             let commission_amount = frm.doc.price_per_night * (frm.doc.commission_rate / 100);
//             let amount = frm.doc.price_per_night - commission_amount;

//             frm.set_value('commission_amount', commission_amount);
//             frm.set_value('amount', amount);
//         }
//     }
// });
frappe.ui.form.on('Hotel Booking', {
    price_per_night: function(frm) {
        calculate_booking_amount(frm);
    },
    from_date: function(frm) {
        calculate_booking_amount(frm);
    },
    to_date: function(frm) {
        calculate_booking_amount(frm);
    },
    refresh(frm) {

        if (!frm.is_new()) {
            if (!frm.custom_buttons['Payment']) {
                frm.add_custom_button(__('Payment'), function() {
                    frappe.msgprint(__('Processing Payment...'));
                    frappe.call({
                        method: "travels.api.make_payment_entry_from_hotel",
                        args: {
                            source_name: frm.doc.name
                        },
                        callback: function (r) {
                            if (r.message) {
                                frappe.model.sync(r.message);
                                frappe.set_route("Form", r.message.doctype, r.message.name);
                            }
                        }
                    });

                });
            }
        }
    },
    hotel: function (frm) {
        frm.set_query('room', function () {
            if (frm.doc.hotel) {
                return {
                    filters: {
                        hotel: frm.doc.hotel // تصفية الغرف بناءً على الفندق المختار
                    }
                };
            }
        });
    },
    country: function (frm) {
        frm.set_query('hotel', function () {
            let filters = {};

            // إذا تم تحديد الدولة
            if (frm.doc.country) {
                filters.country = frm.doc.country;
            }

            // إذا تم تحديد المدينة
            if (frm.doc.city) {
                filters.city = frm.doc.city;
            }

            return {
                filters: filters
            };
        });
    },
    city: function (frm) {
        frm.trigger('country'); // إعادة تطبيق الفلتر إذا تم تعديل المدينة
    }
});

function calculate_booking_amount(frm) {
    if (frm.doc.from_date && frm.doc.to_date && frm.doc.price_per_night) {
        // حساب عدد الأيام بين التاريخين
        let from_date = frappe.datetime.str_to_obj(frm.doc.from_date);
        let to_date = frappe.datetime.str_to_obj(frm.doc.to_date);
        let days = frappe.datetime.get_diff(to_date, from_date) + 1; // تشمل اليوم الأول

        if (days > 0) {
            // حساب قيمة الحجز
            let booking_amount = days * frm.doc.price_per_night;

            // تحديث الحقول
            frm.set_value('booking_amount', booking_amount);

            // إذا كانت هناك عمولة، قم بحساب مبلغ العمولة والمبلغ المستحق
            if (frm.doc.commission_rate) {
                let commission_amount = booking_amount * (frm.doc.commission_rate / 100);
                let hotel_amount = booking_amount - commission_amount;

                frm.set_value('commission_amount', commission_amount);
                frm.set_value('hotel_amount', hotel_amount); // تعديل الحقل إلى hotel_amount
            }
        } else {
            frappe.msgprint(__('The "To Date" must be after "From Date".'));
            frm.set_value('to_date', null);
        }
    }
}


