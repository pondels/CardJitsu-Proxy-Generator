SWF_DIR := './files/swf_files'
SWF_JSON := './scrape/swf_links.json'
IMAGE_FILE_DIR := './downloaded_cards'
SWF_FILE_PATH := $(SWF_DIR)/1.swf

string_filter := $(firstword $(subst "GamesCardIcons", ,$1))

dependencies:
	git clone https://github.com/ruffle-rs/ruffle.git

download_swf_files: #| $(SWF_DIR)
	cd $(SWF_DIR) && \
	python3.14 -c 'import json; [print(k, v, v.split("/")[-1]) for k, v in json.load(open("../../$(SWF_JSON)")).items()]' | \
	while read -r card_number download_link file_name; do \
		echo $$card_number; \
		echo $$download_link; \
		echo $$file_name; \
		curl -O $$download_link; \
		mv $$file_name $$card_number.swf; \
	done

$(SWF_DIR):
	cd ./files && mkdir swf_files

$(IMAGE_FILE_DIR):
	mkdir $(IMAGE_FILE_DIR)

# .PHONY extract
extract_png_from_swf:# | $(IMAGE_FILE_DIR)
	cd ./ruffle && \
	for f in ../$(SWF_DIR)/*; do \
		python3.14 -c 'print("$(SWF_FILE_PATH)")' | \
		while read -r trunc_path; do \
			echo $$trunc_path; \
		done \
    done
	@echo Hi;

# python3.14 -c 'print(str($($$f)).split("/")[-1].split(".")[0])' | \
# cargo run --release --package=exporter -- --width 1024 --height 1024 $$f ../$(IMAGE_FILE_DIR)/$().png; \

clean:
	rm -r ./files/swf_files
	rm -r ./files/CardImages

# all: extract_png_from_swf
# all: dependencies download_swf_files extract_png_from_swf
# all: extract_png_from_swf