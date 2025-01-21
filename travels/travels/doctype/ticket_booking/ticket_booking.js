// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Ticket Booking', {

    refresh(frm) {

        if (!frm.is_new()) {
            if (!frm.custom_buttons['Payment']) {
                frm.add_custom_button(__('Payment'), function() {
                    frappe.msgprint(__('Processing Payment...'));
                    frappe.call({
                        method: "travels.api.make_payment_entry_from_ticket",
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


    validate: function (frm) {
        let total_preferences_amount = 0;

        // جمع جميع القيم داخل جدول preference
        if (frm.doc.preference && frm.doc.preference.length > 0) {
            frm.doc.preference.forEach(row => {
                total_preferences_amount += row.amount || 0; // إذا كان الحقل فارغًا، استخدم 0
            });
        }

        // جمع قيمة trip_price مع المجموع من جدول preference
        let total_ticket_amount = total_preferences_amount + (frm.doc.trip_price || 0);

        // تحديث حقل total_ticket_amount
        frm.set_value('total_ticket_amount', total_ticket_amount);
    },


    ticket_type: function(frm) {
        
        if (frm.doc.trip) {
            frappe.db.get_doc('Trip', frm.doc.trip).then(doc => {
                let price = 0;

                if (frm.doc.ticket_type === "One Way") {
                    price = doc.price_for_one_way || 0;
                } else if (frm.doc.ticket_type === "Return") {
                    price = doc.price_for_return || 0;
                } else if (frm.doc.ticket_type === "Round Trip") {
                    price = doc.price_for_round_trip || 0;
                }

                frm.set_value('trip_price', price);
                frm.fields_dict['trip_price'].df.hidden = false;
                frm.refresh_field('trip_price');
            });
        } else {
            frm.set_value('trip_price', 0);
        }
    },

    trip: function(frm) {
        // trip: function (frm) {
            frm.trigger('ticket_type'); // تنفيذ أي منطق متعلق بـ ticket_type
    
            if (frm.doc.trip) {
                // جلب تفاصيل الرحلة المختارة
                frappe.db.get_doc('Trip', frm.doc.trip)
                    .then(trip => {
                        if (frm.doc.trip_type === 'Flight') {
                            // إذا كانت الرحلة من نوع Flight
                            if (trip.airline) {
                                // جلب تفاصيل شركة الطيران
                                frappe.db.get_doc('Airline', trip.airline)
                                    .then(airline => {
                                        frm.set_value('commission_rate', airline.commission_rate || 0)
                                            .then(() => {
                                                calculate_commission_and_total(frm);
                                            });
                                    });
                            } else {
                                // إذا لم تكن هناك شركة طيران مرتبطة
                                frm.set_value('commission_rate', 0)
                                    .then(() => {
                                        calculate_commission_and_total(frm);
                                    });
                            }
                        } else if (frm.doc.trip_type === 'Road Trip') {
                            // إذا كانت الرحلة من نوع Road Trip
                            if (trip.rental_company) {
                                // جلب تفاصيل شركة النقل أو الإيجار
                                frappe.db.get_doc('Transport or Rental Company', trip.rental_company)
                                    .then(rental_company => {
                                        frm.set_value('commission_rate', rental_company.commission_rate || 0)
                                            .then(() => {
                                                calculate_commission_and_total(frm);
                                            });
                                    });
                            } else {
                                // إذا لم تكن هناك شركة نقل مرتبطة
                                frm.set_value('commission_rate', 0)
                                    .then(() => {
                                        calculate_commission_and_total(frm);
                                    });
                            }
                        } else {
                            // إذا لم يتم تحديد نوع الرحلة
                            frm.set_value('commission_rate', 0)
                                .then(() => {
                                    calculate_commission_and_total(frm);
                                });
                        }
                    });
            } else {
                // إذا لم يتم اختيار أي رحلة
                frm.set_value('commission_rate', 0)
                    .then(() => {
                        calculate_commission_and_total(frm);
                    });
            }
    },

    total_amount: function (frm) {
        calculate_commission_and_total(frm);
    },
    
    commission_rate: function (frm) {
        calculate_commission_and_total(frm);
    }
    
});

// دالة لحساب العمولة والمبلغ النهائي
function calculate_commission_and_total(frm) {
    if (frm.doc.total_amount && frm.doc.commission_rate) {
        const commission_amount = (frm.doc.total_amount * frm.doc.commission_rate) / 100;

        const total_amount = frm.doc.total_ticket_amount - commission_amount;

        frm.set_value('commission_amount', commission_amount);
        frm.set_value('total_amount', total_amount);
    } else {
        frm.set_value('commission_amount', 0);
        frm.set_value('total_amount', frm.doc.total_amount || 0);
    }
};
