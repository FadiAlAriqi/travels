frappe.ui.form.on("Booking Services", {
    refresh(frm) {
        // frm.trigger("calculate_display_amount"); // حساب المجموع عند تحديث النموذج
        // frm.trigger("calculate_total_rental_vehicles_amount");
        // frm.trigger("calculate_total_hotels_amount");
        // frm.trigger("calculate_total_tickets_amount");
        // frm.trigger("calculate_total");
        if (frm.doc.docstatus == 1 ) {
            frm.events.show_general_ledger(frm);
            erpnext.accounts.ledger_preview.show_accounting_ledger_preview(frm);
        };

        frm.fields_dict['ticket'].grid.get_field('ticket').get_query = function () {
            return {
                filters: {
                    name: null
                }
            };
        };

        frm.fields_dict['hotel'].grid.get_field('hotel').get_query = function () {
            return {
                filters: {
                    name: null
                }
            };
        };

        frm.fields_dict['vehicle'].grid.get_field('vehicle').get_query = function () {
            return {
                filters: {
                    name: null
                }
            };
        };
    },
         
        
            show_general_ledger: function(frm) {
                frm.add_custom_button(
                    __("Ledger"),
                    function () {
                        frappe.route_options = {
                            voucher_no: frm.doc.name,
                        };
                        frappe.set_route("query-report", "General Ledger");
                    },
                    "fa fa-table"
                );


        if (frm.doc.docstatus === 1) {
            if (!frm.custom_buttons['Payment']) {
                frm.add_custom_button(__('Payment'), function() {
                    frappe.msgprint(__('Processing Payment...'));
                    frappe.call({
                        method: "travels.api.make_payment_entry",
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

    calculate_total_rental_vehicles_amount(frm) {
        let total = 0;

        for (let item of frm.doc.vehicle) {
            total += item.booking_amount || 0;
        }

        frm.set_value("total_rental_vehicles_amount", total);
    },


    calculate_total_hotels_amount(frm) {
        let total = 0;

        for (let item of frm.doc.hotel) {
            total += item.booking_amount || 0;
        }

        frm.set_value("total_hotels_amount", total);
    },


    calculate_total_tickets_amount(frm) {
        let total = 0;

        for (let item of frm.doc.ticket) {
            total += item.total_ticket_amount || 0;
        }

        frm.set_value("total_tickets_amount", total);
    },


    calculate_total(frm) {
        let total = 0;

        total = total + ( frm.doc.total_rental_vehicles_amount || 0 ) + ( frm.doc.total_hotels_amount || 0 ) + ( frm.doc.total_tickets_amount || 0);

        frm.set_value("total", total);
    },


});

frappe.ui.form.on("Vehicle Rental Package", {

    vehicle(frm, cdt, cdn) {
        frm.trigger("calculate_total_rental_vehicles_amount");
        frm.trigger("calculate_total");
    },

    vehicle_remove(frm) {
        frm.trigger("calculate_total_rental_vehicles_amount");
        frm.trigger("calculate_total");
    },
});


frappe.ui.form.on("Hotel Rental Package", {
    refresh: function(frm) {
        frm.fields_dict['hotel'].grid.add_custom_button(__('Make Payment'), function() {
            let selected_row = frm.fields_dict['Hotel'].grid.get_selected_children()[0];
            if (selected_row) {
                frappe.call({
                    method: 'travels.api.make_payment_entry',
                    args: {
                        source_name: selected_row.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            frappe.set_route('Form', 'Payment Entry', r.message.name);
                        }
                    }
                });
            } else {
                frappe.msgprint(__('Please select a row first.'));
            }
        });
    },


    hotel(frm, cdt, cdn) {
        frm.trigger("calculate_total_hotels_amount");
        frm.trigger("calculate_total");
    },

    hotel_remove(frm) {
        frm.trigger("calculate_total_hotels_amount");
        frm.trigger("calculate_total");
    },
    payment: function(frm, cdt, cdn) {
        // احصل على بيانات الصف المحدد
        let row = frappe.get_doc(cdt, cdn);

        // تحقق من وجود اسم الفندق
        if (!row.hotel) {
            frappe.msgprint(__('Please select a Hotel before making a payment.'));
            return;
        }

        // استدعاء دالة Python لإنشاء Payment Entry
        frappe.call({
            method: "travels.api.make_payment_entry",
            args: {
                source_name: cur_frm.doc.name, // اسم السجل الحالي
                hotel_name: row.hotel_name     // اسم الفندق من الجدول
            },
            callback: function (r) {
                if (r.message) {
                    frappe.set_route("Form", "Payment Entry", r.message.name);
                }
            }
        });
        
    }
    // payment: function (frm, cdt, cdn) {
    //     let row = frappe.get_doc(cdt, cdn); // جلب بيانات الصف المحدد
    
    //     // التحقق من أن الصف يحتوي على البيانات المطلوبة
    //     if (row) {
    //         frappe.new_doc('Payment Entry', {
    //             party_type: 'Supplier', // يمكنك التغيير إلى قيمة ديناميكية إذا لزم الأمر
    //             party: row.supplier_name || "Al-Ola", // استخدم الحقل المناسب من الصف
    //         });
    //     } else {
    //         frappe.msgprint(__('لا يمكن العثور على بيانات الصف المحدد.'));
    //     }
    // }
});

frappe.ui.form.on("Tickets Package", {

    ticket(frm, cdt, cdn) {
        frm.trigger("calculate_total_tickets_amount");
        frm.trigger("calculate_total");
    },

    ticket_remove(frm) {
        frm.trigger("calculate_total_tickets_amount");
        frm.trigger("calculate_total");
    },
});
