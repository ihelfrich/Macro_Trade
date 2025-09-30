
set -e
python3 -m pytest -q
python3 trade_model.py --psi 0.5 --epsilon 4
python3 trade_model.py --psi 0.5 --epsilon 4 --theta 0.3
python3 trade_model.py --psi 0.5 --epsilon 4 --heatmap
