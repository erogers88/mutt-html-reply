import argparse
import email
import html
import sys
from bs4 import BeautifulSoup, Doctype
import css_inline

HEADER_FIRST_SORT_LIST_COMPARISON = ['F','D','T','C','S']

def main():
    """
    Create an Outlook-style HTML reply
    """

    # Parse args
    parser = argparse.ArgumentParser(description="Create an Outlook-style HTML reply")
    parser.add_argument("-m", "--message",
                        nargs='?',
                        type=argparse.FileType('r'),
                        help="Original message file")
    parser.add_argument("-r", "--reply",
                        type=argparse.FileType('r'),
                        default=sys.stdin,
                        help="HTML reply, file or defaults to stdin")
    parser.add_argument("-o", "--output",
                        nargs='?',
                        type=argparse.FileType('w'),
                        default=sys.stdout,
                        help="HTML output, file or defaults to stdout")

    args = parser.parse_args()

    # Get text/html
    ## Get the reply html from file/stdin
    html_reply = args.reply.read()

    ## Get the original headers and html from the original email (rfc822 format)
    rfc822_original = email.message_from_file(args.message)
    html_original_msg = _get_message_html(rfc822_original)
    html_headers = _get_header_html(rfc822_original)

    # Convert HTML text to BeautifulSoup object and inline all CSS
    bs4_msg = BeautifulSoup(css_inline.inline(html_reply),'html.parser')

    bs4_original_msg = BeautifulSoup(css_inline.inline(html_original_msg), 'html.parser')
    bs4_original_msg.html.unwrap() #type: ignore
    bs4_original_msg.body.unwrap() #type: ignore
    bs4_original_msg.head.extract() #type: ignore
    for element in bs4_original_msg.contents:
        if isinstance(element, Doctype):
            element.extract()

    bs4_original_headers = BeautifulSoup(html_headers, 'html.parser')

    # Combine HTML together
    bs4_final = bs4_msg
    bs4_final.body.append(BeautifulSoup('<hr></hr>', 'html.parser')) #type: ignore
    bs4_final.body.append(bs4_original_headers) #type: ignore
    bs4_final.body.append(bs4_original_msg) #type: ignore

    # Write output
    args.output.write(str(bs4_final))


def _get_header_html(message):
    #resorted_text = []
    #for first in HEADER_FIRST_SORT_LIST_COMPARISON:
    #    for header in header_list:
    #        if header[0] == first:
    #            resorted_text.append(html.escape(header))
    #html_headers = "<p>"
    #for header in resorted_text:
    #    html_headers = html_headers + '<br>' + header
    #html_headers = html_headers + "</p>\n"
    return "<hr><p>test headers html</p>"


def _get_message_html(message):
    return "<hr><p>test original message html</p>"

if __name__ == "__main__":
    main()
