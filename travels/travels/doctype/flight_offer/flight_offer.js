// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Flight Offer", {
	// refresh(frm) {

    //     frappe.call({
    //         method: "travels.api.fetch_and_store_flight_offers",
    //         callback: function(response) {
    //             frappe.msgprint(response.message);
    //         }
    //     });
        

	// },
});
// frappe.listview_settings['Flight Offer'] = {
//     onload: function(listview) {
//         frappe.call({
//             method: "travels.api.fetch_and_store_flight_offers",
//             callback: function(response) {
//                 if (response.message) {
//                     frappe.msgprint(__('Flight offers fetched successfully!'));
//                     // يمكنك تحديث القائمة مباشرة إذا لزم الأمر
//                     listview.refresh();
//                 }
//             },
//             error: function(err) {
//                 frappe.msgprint(__('Failed to fetch flight offers. Please try again.'));
//             }
//         });
//     }
// };
