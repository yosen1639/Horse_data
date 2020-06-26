import move
import pandas as pd

Arima_final = move.main()
filename = 'Nakayama_female.xlsx'
Arima_final.to_excel(filename)

