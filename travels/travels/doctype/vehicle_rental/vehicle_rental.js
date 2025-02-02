// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle Rental", {
	refresh(frm) {

        if (!frm.is_new()) {
            if (!frm.custom_buttons['Payment']) {
                frm.add_custom_button(__('Payment'), function() {
                    frappe.call({
                        method: "travels.api.make_payment_entry_from_transport_company",
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

    company: function (frm) {
        filter_vehicles(frm);
    },
    
    vehicle_type: function (frm) {
        filter_vehicles(frm);
    },

    rental_start_date: function(frm) {
        calculate_total_rate(frm);
        calculate_days(frm);
        calculate_booking_amount(frm);

    },

    rental_end_date: function(frm) {
        calculate_total_rate(frm);
        calculate_days(frm);
        calculate_booking_amount(frm);
    },

    daily_rental_price: function(frm) {
        calculate_total_rate(frm);
        calculate_booking_amount(frm);
    }
});


function filter_vehicles(frm) {
    const company = frm.doc.company;
    const vehicle_type = frm.doc.vehicle_type;

    let filters = {};

    if (company) {
        filters["company"] = company;
    }

    if (vehicle_type && vehicle_type !== '') {
        filters["type"] = vehicle_type;
    }

    frm.set_query('vehicle', function () {
        return {
            filters: filters
        };
    });
}


function calculate_days(frm){
    if (frm.doc.rental_start_date && frm.doc.rental_end_date) {
        const fromDate = new Date(frm.doc.rental_start_date);
        const toDate = new Date(frm.doc.rental_end_date);
        
        const diffInTime = toDate.getTime() - fromDate.getTime();
        const days = diffInTime / (1000 * 3600 * 24);

        frm.set_value('days', days); 
}
}


function calculate_total_rate(frm) {
    if (frm.doc.rental_start_date && frm.doc.rental_end_date) {
        const fromDate = new Date(frm.doc.rental_start_date);
        const toDate = new Date(frm.doc.rental_end_date);
        
        const diffInTime = toDate.getTime() - fromDate.getTime();
        const days = diffInTime / (1000 * 3600 * 24);

        // const days = calculate_days(frm);

        const daily_rental_price = frm.doc.daily_rental_price || 0;

        frm.set_value('booking_amount', daily_rental_price * days); 
    }
}


function calculate_booking_amount(frm) {
    if (frm.doc.days > 0) {
        let booking_amount = frm.doc.days * frm.doc.daily_rental_price;

        frm.set_value('booking_amount', booking_amount);

        if (frm.doc.commission_rate) {
            let commission_amount = booking_amount * (frm.doc.commission_rate / 100);
            let rental_company_amount = booking_amount - commission_amount;

            frm.set_value('commission_amount', commission_amount);
            frm.set_value('rental_company_amount', rental_company_amount);
        }
    }
    
    // else {
    //     frappe.msgprint(__('The "Start Date" must be after "End Date".'));
    //     frm.set_value('rental_end_date', null);
    // }
}



