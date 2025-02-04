// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Booking Service', {
    ticket_booking: function(frm) {
        frappe.new_doc('Ticket Booking'); // فتح نموذج جديد

        // انتظر قليلاً حتى يفتح النموذج، ثم قم بتحديث الحقل يدويًا
        setTimeout(() => {
            frappe.ui.form.on('Ticket Booking', {
                onload: function(childFrm) {
                    if (childFrm.doc.trip) {
                        frappe.db.get_doc('Trip', childFrm.doc.trip).then(doc => {
                            let price = 0;
                            if (childFrm.doc.ticket_type === "One Way") {
                                price = doc.price_for_one_way || 0;
                            } else if (childFrm.doc.ticket_type === "Return") {
                                price = doc.price_for_return || 0;
                            } else if (childFrm.doc.ticket_type === "Round Trip") {
                                price = doc.price_for_round_trip || 0;
                            }

                            childFrm.set_value('trip_price', price);
                            childFrm.fields_dict['trip_price'].df.hidden = false;
                            childFrm.refresh_field('trip_price');
                        });
                    } else {
                        childFrm.set_value('trip_price', 0);
                    }
                }
            });
        }, 500); // تأخير لضمان فتح النموذج أولاً
    }
});



