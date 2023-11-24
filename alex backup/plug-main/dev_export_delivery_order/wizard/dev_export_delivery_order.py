 # -*- coding: utf-8 -*-
##############################################################################
#    
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Devintelle Solutions (<http://devintellecs.com/>).
#
##############################################################################

from odoo import  fields, models, _
#========For Excel=======
from io import BytesIO
import xlwt
from xlwt import easyxf
import base64
# =======================

class dev_export_delivery_order(models.TransientModel):
    _name = "dev.export.delivery.order"
    
    name = fields.Char('Name')
    excel_file = fields.Binary('Excel File')
    

    def get_partner_address(self,partner):
        name = ''
        if partner:
            name = partner.name + '\n'
            if partner.street:
                name = name + partner.street + '\n'
            if partner.street2:
                name = name + partner.street2 + '\n'
            city = ''
            if partner.city:
                city = partner.city 
            if partner.zip:
                if city:
                    city = city + ', '+ partner.zip
            if city:
                name = name + city +'\n'
                
            if partner.state_id:
                name = name + partner.state_id.name + '\n'
            if partner.country_id:
                name = name + partner.country_id.name + '\n'
        return name 

    def create_excel_header(self,picking,worksheet):
        header_style = easyxf('font:height 300;pattern: pattern solid, fore_color 0x3F; align: horiz center;font:bold True;')
        sub_header = easyxf('font:height 210;pattern: pattern solid, fore_color silver_ega;font:bold True;')
        content = easyxf('font:height 200;')

        if picking.picking_type_id.code == 'outgoing':
            worksheet.write_merge(2, 3, 2, 4, 'Delivery Order : '+ picking.name, header_style)
        elif picking.picking_type_id.code == 'incoming':
            worksheet.write_merge(2, 3, 2, 4, 'Receipt : '+ picking.name, header_style)
        else:
            worksheet.write_merge(2, 3, 2, 4, 'Internal Move : '+ picking.name, header_style)

        if picking.partner_id:
            name = self.get_partner_address(picking.partner_id)
            worksheet.write_merge(5, 5, 0, 1,'Address', sub_header)
            worksheet.write_merge(6, 11, 0, 1,name, content)

        row = 5
        if picking.scheduled_date:
            worksheet.write(row, 4, 'Scheduled Date', sub_header)
            date = picking.scheduled_date.strftime("%d-%m-%Y %H:%M:%S")
            worksheet.write_merge(row, row, 5, 6, date, content)
            row+=1
        if picking.origin:
            worksheet.write(row, 4,'Origin', sub_header)
            worksheet.write_merge(row, row, 5, 6, picking.origin, content)
            row+=1
        if picking.company_id:
            worksheet.write(row, 4, 'Company', sub_header)
            worksheet.write_merge(row, row, 5, 6, picking.company_id.name, content)
            row+=1
        if picking.picking_type_id:
            picking_code = picking.picking_type_id.code
            if picking_code == 'incoming':
                picking_type = 'Incoming'
            elif picking_code == 'outgoing':
                picking_type = 'Outgoing'
            else:
                picking_type = 'Internal'

            worksheet.write(row, 4,'Type', sub_header)
            worksheet.write_merge(row, row, 5, 6, picking_type, content)
            row+=1

        worksheet.write(13, 0, 'Default Code', sub_header)
        worksheet.write_merge(13,13, 1, 2, 'Product', sub_header)
        worksheet.write(13, 3, 'Initial Demand', sub_header)
        worksheet.write(13, 4, 'Done Qty', sub_header)
        worksheet.write(13, 5, 'UOM', sub_header)
        row = 13
        ini_total = 0
        done_total = 0
        for line in picking.move_lines:
            ini_total += line.product_uom_qty
            done_total += line.quantity_done
            row +=1
            worksheet.write(row, 0, line.product_id.default_code or '', content)
            worksheet.write_merge(row,row, 1,2,  line.product_id.name or ' ', content)
            worksheet.write(row, 3, line.product_uom_qty, content)
            worksheet.write(row, 4, line.quantity_done, content)
            worksheet.write(row, 5, line.product_uom.name or '', content)
        
        row+=1
        worksheet.write(row,2, 'Total', sub_header)
        worksheet.write(row,3, ini_total, sub_header)
        worksheet.write(row,4, done_total, sub_header)
        row+=1

        return worksheet, row+1     
            
    def export_delivery_order(self):
        workbook = xlwt.Workbook()
        filename = 'Delivery Order.xls'
        active_ids = self._context.get('active_ids')
        model_pool = self.env[self._context.get('active_model')]
        worksheet = []
        count = 0
        for i in active_ids:
            worksheet.append(count)
            count+=1
        
        picking_ids = model_pool.browse(active_ids)
        
        c = -1
        for picking in picking_ids:
            c +=1
            worksheet[c] = workbook.add_sheet(picking.name)
            worksheet[c].col(0).width = 130 * 30
            worksheet[c].col(1).width = 130 * 30
            worksheet[c].col(2).width = 130 * 30
            worksheet[c].col(3).width = 130 * 30
            worksheet[c].col(4).width = 130 * 33
            worksheet[c].col(5).width = 130 * 30

            worksheet[c],row = self.create_excel_header(picking,worksheet[c])

        fp = BytesIO()
        workbook.save(fp)
        fp.seek(0)
        excel_file = base64.encodestring(fp.read())
        fp.close()
        self.write({'excel_file': excel_file})

        if self.excel_file:
            active_id = self.ids[0]
            return {
                'type': 'ir.actions.act_url',
                'url': 'web/content/?model=dev.export.delivery.order&download=true&field=excel_file&id=%s&filename=%s' % (
                    active_id, filename),
                'target': 'new',
            }
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
