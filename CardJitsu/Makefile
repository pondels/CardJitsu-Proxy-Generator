SWF_DIR := './files/swf_files'
SWF_JSON := './scrape/swf_links.json'
IMAGE_FILE_DIR := './downloaded_cards'

dependencies:
	git clone https://github.com/ruffle-rs/ruffle.git

download_swf_files: $(SWF_DIR)
	cd $(SWF_DIR) && \
	python3.14 -c 'import json; [print(k, v, v.split("/")[-1]) for k, v in json.load(open("../../$(SWF_JSON)")).items()]' | \
	while read -r card_number download_link file_name; do \
		echo $$card_number; \
		echo $$download_link; \
		echo $$file_name; \
		curl -O $$download_link; \
		mv $$file_name $$card_number.swf; \
		cd ../../ruffle; \
		cargo run --release --package=exporter -- --width 1024 --height 1024 ../$(SWF_DIR)/$$card_number.swf ../$(IMAGE_FILE_DIR)/$$card_number.png; \
		cd ../$(SWF_DIR); \
	done

$(SWF_DIR):
	cd ./files && mkdir swf_files

python_setup:
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt
	python3 generate.py

clean:
	rm -r ./files/swf_files
	rm -r venv

all: dependencies download_swf_files python_setup