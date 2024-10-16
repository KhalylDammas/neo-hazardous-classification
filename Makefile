# Create new branch 
branch: #cheacked 🙏
	git checkout -b $(name) && \
	git branch
# make branch name=<branch_name>

#make commit
commit: #cheacked 🙏
	@if [ -f $(file) ]; then \
		git add $(file) && git commit -m "$(message)" && git push origin $(name); \
	else \
		echo "Error: $(file) does not exist!"; \
	fi 
# make commit file=<file_name> message="your message here" name=<branch_name>

#commit somthing wrong 
undo: #cheacked 🙏
	git restore --staged $(file) && \
	git restore $(file)
# make undo <name_of_the_file_you_commited_wrong>

#update local branch 
update: #cheacked 🙏
	@echo "Updating local master branch..."
	git checkout master && \
	git pull origin master 
# make update

install:
	@pip install -e . 
	@pip install -r requirements.txt
# make install

# Upgrade dependencies
update_dep:
	@echo "Upgrading installed packages..."
	@pip install --upgrade -e . 
	@pip install --upgrade -r requirements.txt