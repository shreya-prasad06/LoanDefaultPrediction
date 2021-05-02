import requests

url = 'http://localhost:5000/results'
r = requests.post(url,json={'loan_amnt':5000,'funded_amnt':5000,'funded_amnt_inv':4975,'term':36,'int_rate':10,'home_ownership':1,'annual_inc':1896,'purpose':1,'total_pymnt':5861,'total_rec_prncp':50000,'total_rec_int':861})

print(r.json())
