.PHONY: all clean
all: 
	data/processed/nj_clean.xlsx
clean:
	rm -f data/processed/*.csv
reshape:
	python data/reshape_data.py
train:
	python models/train_model.py
predict:
	python models/predict_model.py
viz:
	python visualizations/make_visualizations.py
