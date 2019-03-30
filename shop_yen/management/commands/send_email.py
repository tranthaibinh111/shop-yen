#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Insert customer info from excel file'

    def handle(self, *args, **options):
        from_email = "Yến Vàng Miền Name <sport@yenvangmiennam.com>"
        to_email = "binh.tt@hdwebsoft.co"

        subject = "[Sức Khỏe] Yến sào Minh Quang"
        content = """
        Mọi người có nhu cầu mua yến ủng hộ em với nhe ^_^.

        🔔CƠ SỞ NUÔI VÀ CHẾ BIẾN YẾN SÀO MINH QUANG📣
        💯Yến Sào Minh Quang đảm bảo uy tín, chất lượng và hiện nay được nhiều quí khách hàng tin dùng.
        💯Có mã vạch quốc tế.
        💯Có đầy đủ các loại giấy tờ về an toàn thực phẩm và giấy phép kinh doanh hợp pháp theo qui định của pháp luật Việt Nam.
        ⭕️Quí khách hàng có nhu cầu xin liên hệ Phạm Ngân 0395735218 ⭕️
        📬Địa chỉ:
        🚦26/16/16 Tân Thới Nhất 2, phường Tân Thới Nhất, quận 12, tp Hồ Chí Minh.
        🚦Giao hàng toàn quốc (Free Ship tại Tp. Hồ Chí Minh)
        💎 YẾN SÀO MINH QUANG TRÂN TRỌNG KÍNH MỜI💎
        #yensao #minhquang #yensaominhquang #hochiminhcity #hochiminh #baclieu #kiengiang #nestbird #health
        """

        response = send_mail(
            subject=subject,
            message=content,
            from_email=from_email,
            recipient_list=[to_email]
        )

        print(response)
