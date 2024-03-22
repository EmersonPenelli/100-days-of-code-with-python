import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib

load_dotenv(".env")
MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

URL = "https://www.amazon.com.br/C%C3%B3digo-limpo-Robert-C-Martin/dp/8576082675/ref=sr_1_1?__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3DVV4UBSHQJ7G&dib=eyJ2IjoiMSJ9.N1gRYrmJjm7IjGH3CvHh2gp4cQYFkQFGKBO2a79rtx9p1umFH0OQGQZxUG68uBiwtgnqxRQ-5ke12KtWESrPI4Cvtr2UQgpMsVxwuv_Wzyb_hGRk7fGkEuILJ7y2Xctb6FUCmH2GCnOUmQv54iJ5MXUEyuYES_fl8Yo94AAy_z4hitteAuz8jjqIEZDiR50PbIH0xrOPOJ8QgRRZ1gef9h00Zs5oG8s8-LeSGEqdyQGci2CPiE7a1CTKSSIrB6x2UJ_d_2IJa-oe0K99IYS4zZACdF70LbL6q9GlDUOx22c.BfVYumUrjZcxLfJHObTmRLrI9GrWU4tKt__7bFhFgys&dib_tag=se&keywords=clean+code&qid=1711113438&sprefix=clean+cod%2Caps%2C244&sr=8-1"
http_headers = {
    "Accept-Language": "pt-BR,pt;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/99.0.4844.51 Safari/537.36",
}
response = requests.get(URL, headers=http_headers)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")

price_element = soup.find(name="span", class_="a-offscreen")
if price_element:
    price = float(price_element.getText()[1:])
    product_name = " ".join(soup.find(name="span", class_="a-size-large product-title-word-break", id="productTitle").getText().split())

    if price < 25.00:
        with smtplib.SMTP("smtp.outlook.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TO_EMAIL,
                msg=f"Subject: Alert: Amazon Price Tracker\n\n{product_name}\nis now ${price}.\n\n{URL}",
            )
else:
    print("Price element not found.")
