// Copyright (c) 2025, YemenFrappe and contributors
// For license information, please see license.txt

frappe.ui.form.on("Hotel", { 
    refresh(frm) { 
        var link = frm.doc.website; 
        if (link != null && link != "") { 
            frm.add_web_link(frm.doc.website); 
        } 
 
    }, 
});
