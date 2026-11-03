.PHONY: sidebar check new serve

# Regenerate docs/_sidebar.md from the files in docs/
sidebar:
	python3 scripts/side_generator.py

# Validate every page against templates/page.md
check:
	python3 scripts/check_pages.py

# Create a page from the template: make new SECTION=linux TITLE="Systemd"
new:
	python3 scripts/new_page.py "$(SECTION)" "$(TITLE)"

# Preview the site at http://localhost:3000
serve:
	python3 -m http.server 3000
