from odoo import models,fields,api
import barcode 
from barcode.writer import ImageWriter
import logging
from bahttext import bahttext
from datetime import datetime
import math
_logger = logging.getLogger(__name__)

class sale_order(models.Model):
    _inherit = 'sale.order'


    def print_quotation(self):
        self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        _logger.info("Call")
        return self.env.ref('custom_apple_start_report.custom_report_saleorder_apple_star').report_action(self)
    
    def baht_text(self,number):
        return bahttext(number)
    
    def ceil(self,number1,number2):
        _logger.info("total page :"+str(math.ceil(number1/number2)))
        _logger.info(number1)
        _logger.info(number2)
        return math.ceil(number1/number2)
    
    def convert_thai_month(self,month):
        _TH_FULL_MONTHS = [
            "มกราคม",
            "กุมภาพันธ์",
            "มีนาคม",
            "เมษายน",
            "พฤษภาคม",
            "มิถุนายน",
            "กรกฎาคม",
            "สิงหาคม",
            "กันยายน",
            "ตุลาคม",
            "พฤศจิกายน",
            "ธันวาคม",
        ]
        return _TH_FULL_MONTHS[month]

    def compute_full_date_thai(self,origin_datetime):
        month_id = int(origin_datetime.strftime('%m'))-1
        month_text = self.convert_thai_month(month_id)
        year_thai = int(origin_datetime.strftime('%Y'))+543
        return str(origin_datetime.strftime('%d')) +"  "+month_text + "  " + str(year_thai)
    
    def get_lines(self,data,max_line):
        line_count = data.count("\n")
        if not line_count:
            if not len(data) % max_line:
                line_count = len(data) / max_line
            else:
                line_count = len(data) / max_line + 1
        elif line_count:
            line_count += 1
            data_line_s = data.split('\n')
            for x in range(0, len(data_line_s),1):
                if len(data_line_s[x]) > max_line:
                    line_count += len(data_line_s[x]) / max_line
        if line_count > 1:
            line_count = line_count * 0.8
        return line_count
    
    def log_start(self,start):
        _logger.info(start)
        return 1

    def get_break_line(self, max_body_height, new_line_height, row_line_height, max_line_lenght):
        print("\n get_break_line====")
        print("\n max_body_height====", max_body_height)
        print("\n new_line_height====", new_line_height)
        print("\n row_line_height====", row_line_height)
        print("\n max_line_lenght====", max_line_lenght)
        break_page_line = []
        count_height = 0
        count = 1

        for line in self.order_line:

            # count += 1
            print(count)
            print(line.product_id.default_code)
            print(line.name)
            line_name = self.get_lines(line.name, max_line_lenght)
            # remove by row height to line
            # line_height = row_line_height + ((self.get_line(line.name, max_line_lenght)) * new_line_height)
            line_height = row_line_height * line_name
            count_height += line_height
            if count_height > max_body_height:
                break_page_line.append(count - 1)
                count_height = line_height
            count += 1
        # last page
        break_page_line.append(count - 1)

        print("\n break_page_line====", break_page_line)
        return break_page_line