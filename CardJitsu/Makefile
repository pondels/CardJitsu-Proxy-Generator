SWF_DIR := './files/swf_files'
SWF_JSON := './scrape/swf_links.json'
IMAGE_FILE_DIR := './downloaded_cards'

dependencies:
	git clone https://github.com/ruffle-rs/ruffle.git

download_swf_files: $(SWF_DIR)
	@cd $(SWF_DIR) && \
	python3.14 -c 'import json; [print(k, v, v.split("/")[-1]) for k, v in json.load(open("../../$(SWF_JSON)")).items()]' | \
	while read -r card_number download_link file_name; do \
		if [ ! -e "$$card_number.swf" ]; then \
			case $$download_link in \
				https://archives.clubpenguinwiki.info*) \
				curl -O $$download_link; \
				mv $$file_name $$card_number.swf; \
				;; \
			*) \
				echo $$download_link; \
				wget -m $$download_link; \
				mv ./icerink.solero.me/src/media1.clubpenguin.com/play/v2/content/global/clothing/photos/$$card_number.swf ./$$card_number.swf; \
				;; \
			esac; \
		fi; \
		if [ ! -e "../../downloaded_cards/$${card_number}.png" ]; then \
			cd ../../ruffle; \
			cargo run --release --package=exporter -- --width 1024 --height 1024 ../$(SWF_DIR)/$$card_number.swf ../$(IMAGE_FILE_DIR)/$$card_number.png; \
			cd ../$(SWF_DIR); \
		fi; \
	done; \
	rm -r ./icerink.solero.me

$(SWF_DIR):
	@if [ ! -d $(SWF_DIR) ]; then \
		cd ./files && mkdir swf_files; \
	fi

python_setup:
	if [ ! -d ./venv ]; then \
		python3 -m venv venv; \
	fi
	. venv/bin/activate && pip install -r requirements.txt
	python3 generate.py

clean:
	rm -r ./files/swf_files

all: dependencies download_swf_files python_setup