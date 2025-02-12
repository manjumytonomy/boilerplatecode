import os
import html.parser
import xlsxwriter
import shutil
import filecmp
#/Users/Manju/Downloads/Carolina East 12-19-24 Epic Test/HTML

class HTMLTagChecker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.mismatched_tags = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        elif self.getpos()[1] < len(self.rawdata) and self.rawdata[self.getpos()[1]] == '<':
            pass  # ignore closing tag if next character is an opening angle bracket
        else:
            self.mismatched_tags.append((self.tag_stack[-1] if self.tag_stack else tag, self.getpos()))

    def get_mismatched_tags(self):
        return self.mismatched_tags

def check_html_file(file_path):
    parser = HTMLTagChecker()
    with open(file_path, 'r') as file:
        parser.feed(file.read())
    return parser.get_mismatched_tags()

def generate_error_report(directory_path):
    issue_count = 0
    report_data = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory_path)
                mismatched_tags = check_html_file(file_path)
                if mismatched_tags:
                    issue_count += 1
                    for tag, pos in mismatched_tags:
                        issue_description = f"Mismatched tag: {tag} at line {pos[0]}, column {pos[1]}"
                        report_data.append([file, relative_path, issue_description, f"Line {pos[0]}, Column {pos[1]}"])
    print(f"\nTotal files with issues: {issue_count}")
    write_report_to_excel(report_data, 'errors.xlsx')

def fix_tag_issues(directory_path):
    issue_count = 0
    report_data = []
    destination_path = directory_path + '_fixed'
    shutil.copytree(directory_path, destination_path, dirs_exist_ok=True)
    for root, dirs, files in os.walk(destination_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, destination_path)
                mismatched_tags = check_html_file(file_path)
                if mismatched_tags:
                    issue_count += 1
                    for tag, pos in mismatched_tags:
                        issue_description = f"Mismatched tag: {tag} at line {pos[0]}, column {pos[1]}"
                        report_data.append([file, relative_path, issue_description, f"Line {pos[0]}, Column {pos[1]}"])
                    with open(file_path, 'r+') as fixed_file:
                        fixed_file_content = fixed_file.read()
                        for tag, pos in mismatched_tags:
                            fixed_file_content = fixed_file_content.replace(f'</{tag}>', f'<!-- {tag} closed -->\n</{tag}>', 1)
                        fixed_file.seek(0)
                        fixed_file.write(fixed_file_content)
                        fixed_file.truncate()
    print(f"\nTotal files with issues fixed: {issue_count}")
    write_report_to_excel(report_data, 'fixed_issues.xlsx')

def write_report_to_excel(report_data, file_name):
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'File Name')
    worksheet.write(0, 1, 'Relative Path')
    worksheet.write(0, 2, 'Issue Description')
    worksheet.write(0, 3, 'Line Number/Tag')
    row = 1
    for file, relative_path, issue_description, line_number in report_data:
        worksheet.write(row, 0, file)
        worksheet.write(row, 1, relative_path)
        worksheet.write(row, 2, issue_description)
        worksheet.write(row, 3, line_number)
        row += 1
    workbook.close()

def main():
    directory_path = input("Enter the directory path: ")
    while True:
        print("\nOptions:")
        print("1. Generate error report")
        print("2. Fix tag issues and generate report")
        print("3. Exit")
        option = input("Enter your choice: ")
        if option == '1':
            generate_error_report(directory_path)
        elif option == '2':
            fix_tag_issues(directory_path)
        elif option == '3':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == '__main__':
    main()
