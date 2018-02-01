import vobject
import io
import argparse

parser = argparse.ArgumentParser(description="Converts vcard files to Sipgate compatible CSV")
parser.add_argument('--output', default="output.csv", metavar="output.csv", help='Set output filename')
parser.add_argument('input', metavar="input.vcf", help='Input VCARD file')
args = parser.parse_args()


fd_vcf= io.open(args.input, mode="r", encoding="utf8")
fd_csv= io.open(args.output, mode="w")
fd_csv.write("{0},{1},{2}\n".format("Vorname", "Nachname", "Rufnummer"))

def replaceSpecialCharacters(text):
	chars={'ö':'oe','ä':'ae','ü':'ue', 'ß':'ss', '&':'und', 'Á':'A'}
	newtext=text
	for char in chars:
		newtext = newtext.replace(char,chars[char])
	return newtext


vcards=vobject.readComponents(fd_vcf)
for vcard in vcards:
	name=None
	if "n" in vcard.contents:
		givenname=vcard.n.value.given
		name=vcard.n.value.family
	elif "org" in vcard.contents:
		givenname=""
		name=vcard.org.value[0]
	
	if name != None:
		if "tel" in vcard.contents:
			for tel in vcard.contents["tel"]:
				try:
					fd_csv.write("{0},{1},{2}\n".format(replaceSpecialCharacters(givenname), replaceSpecialCharacters(name), tel.value))
				except:
						print("Some non-ascii characters in the following VCARD:")
						vcard.prettyPrint()
		
		else:
			print("Contact {0} has no phone number".format(vcard.n))
	else:
		print("No Name nor organisation in the following VCARD:")
		vcard.prettyPrint()