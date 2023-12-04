import sys
import subprocess
from pathlib import Path
import glob


def cover_letter(cover_letter_kwargs: dict,
                 template: str='template.txt') -> None:
    """ Generate a cover letter for a company

    Arguments:
        cover_letter_kwargs {dict} -- a dict with the keys company_name, location, position, 
            your_name, your_email, and your_phone_number
        template {str} -- a .txt file containing the skeleton to be used

    Returns:
        None -- writes a .tex file with the arguments filled
    """
    
    print(f'Using template {template}')
    with open(template) as f:
        t = f.read()
    raw_string = r'{}'.format(t)
    filled_string = raw_string.format(**cover_letter_kwargs)
    company_name = cover_letter_kwargs['company_name']
    print(f'Saving {company_name}_cover_letter.tex')
    save_path = Path('cover_letters') / f'{company_name}_cover_letter.tex'
    with open(save_path, 'w') as g:
        g.write(filled_string)


def main():
    company_name = input('What is the company name? ')
    location = input('What is the location e.g. Atlanta? ')
    position = input('What is the name of the position e.g. Data Scientist? ')
    your_name = input('What is your name? ')
    your_email = input('What is your email? ')
    your_phone_number = input('What is your phone number? ')

    kwargs = {'company_name': company_name,
              'location': location,
              'position': position,
              'your_name': your_name,
              'your_phone_number': your_phone_number,
              'your_email': your_email}
    
    cover_letter(kwargs)
    company_name = kwargs['company_name']
    cover_path = Path('cover_letters') / f'{company_name}_cover_letter.tex'
    if sys.platform in ['win32', 'cygwin']:
        latex_name = 'miktex-pdflatex.exe'
    else:
        latex_name = 'pdflatex'
    output = subprocess.check_output(f'which {latex_name}'.split())
    latex_bin = output.decode().strip()
    args_list = [latex_bin] + [str(cover_path)]
    subprocess.run(args_list)
    tex_files = glob.glob(f'{company_name}_cover_letter.*')
    subprocess.run(['mv'] + tex_files + [cover_path.parent])


if __name__ == '__main__':
    main()
