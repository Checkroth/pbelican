Title: Password Protected Files in Python
Date: 2019-04-12
Category: blog
Tags: python, pdf, msoffcrypto-tool, pikepdf
Slug: unlocking-password-protected-files
Authors: Charles Heckroth
<!-- Summary: Stripping passwords from files in Python -->

When working on a system that processes files, you're likely to run in to password protected files. Particularly in Japan, password-protected pdfs, office files, and zip files are the norm.

I turn down feature requests for zip files due to the possibility of them containing an undefined nested directory structure that would be a lot more work than its worth to deal with. So I have no thoughts on dealing with those in python, though [python's zipfile module](https://docs.python.org/3/library/zipfile.html) would almost certainly do the trick.

PDFs and Office Files are a different issue. I use [pikepdf](https://github.com/pikepdf/pikepdf) for pdf processing and [msoffcrypto-tool](https://github.com/nolze/msoffcrypto-tool) for office file processing.

# PDFs and PikePDF

Pikepdf is really, really simple.

```python
import pikepdf
from pathlib import Path

encrypted_file = Path('myfile.pdf')
decrypted_file = Path('pikepdf_output.pdf')
pikepdf.open(encrypted_file, password='my_password')
pikepdf.save(decrypted_file)
```

And that's it! Mostly.

There are three minor points to address:

- Pikepdf will throw errors on decryption
- Pikepdf will not error if you input a password for a file that isn't password-protected
- Pikepdf will not be able to directly overwrite the pdf with its decrypted version

## Handling the errors

Pikepdf will throw errors if you have:

- A file that isn't a pdf
- A broken pdf
- The wrong password

Handling each case is also incredibly simple.

```python
encrypted_file = Path('myfile.pdf')
decrypted_file = Path('pikepdf_output.pdf')
try:
    pikepdf.open(encrypted_file, 'my_password')
    pikepdf.save(decrypted_file)
except pikepdf.PdfError:
    # A file that isn't a pdf
    # A broken pdf
    print('Do something with your not-a-pdf')
except pikepdf.PasswordError:
    # The wrong password
    print('Do something with your password-encrypted pdf that you failed to decrypt')
```

The errors are very simple. A PdfError if Pikepdf couldn't open the file (this is unrelated to encryption itself), and a PasswordError if your password was wrong.

## Finding out if a file is encrypted

Pike pdf will _not_ throw an error if you put in a password for a pdf that has no password. It will just open the file normally.

This is never really an issue, but you might find yourself in a situation where you need to see if a pdf has a password or not.

For instance, maybe you have a password unlock feature in your application. You don't have any passwords when you initially store the PDF, but you do need to flag it as password-protected or not, so your users know if they need to unlock it or not.

```python
try:
    pdf = pikepdf.open(Path('maybe_encrypted_file.pdf'))
    del pdf
    return 'Not encrypted!'
except pikepdf.PasswordError:
    return 'Encrypted!'
```

The PasswordError will be thrown if you _don't_ supply a password to a pdf that is password protected. If you throw a password in and don't get a password error, you don't know if it was initially encrypted or not.

### del pdf?????

`del pdf` is actually unnecessary, but [PikePDF will not automatically close the os handler in some cases](https://github.com/pikepdf/pikepdf/issues/37). Most people don't really have to worry about this, but if you have a high traffic service that uses pikepdf heavily and is not often restarted you may run in to a "Too many open files" error after some time. `del pdf` will delete the variable and its related os handler.

## Overwriting your pdf with pikepdf

Long story short: You can't do it. Save your decrypted file as a separate pdf, and then use `shutil` to move it over the original file.

```python
encrypted_file = Path('myfile.pdf')
decrypted_file = Path('pikepdf_output.pdf')
pdf = pikepdf.open(encrypted_file, password='mypassword')
pdf.save(decrypted_file)
shutil.move(decrypted_file, encrypted_file)
```

It's not pretty, but it works.

# Office Files and msoffcrypto-tool

Msoffcrypto-tool is a bit more complicated than pikepdf.

- Office 97~2004 XLS files are not supported for decryption.
- Each file type and office version will have a different impact on how msoffcrypto tool fails
- msoffcrypto throws generic python errors
    - `OSError`: Not an office file
    - `AssertionError`: Office 97~2004 wrong password input
    - `Exception`: Non-encrypted xls file, OR wrong password input on decrypt
    - `error`: Correct password on encrypted office 97~2004 xls file
  
Its a lot to take in, so I'm just going to put my full code for decrypting an office file when you don't know what kind of office file it is.

```python
# Open the file
from pathlib import Path
import msoffcrypto

full_path = Path('input_file.docx')
out_path = Path('output_file.docx')
with open(full_path, 'rb') as office_in:
    try:
        # Load it in to msoffcrypto
        office_file = msoffcrypto.OfficeFile(office_in)
        office_file.load_key(password=password)
    except OSError:
        # OSError will be thrown if you passed in a file that isn't an office file
        return 'not an office file'
    except AssertionError:
        # Office 97~2004 files only:
        # AssertionError will be thrown on load_key if the password is wrong
        return 'wrong password'
    except Exception:
        # xls files only:
        # msoffcrypto will throw a generic Exception on load_key if the file isn't encrypted
        return 'not encrypted'

    if not office_file.is_encrypted():
        # Other than xls files, you can check if a file is encrypted with the .is_encrypted function
        return 'not encrypted'

    # Open your desired output as a file
    with open(out_path, 'wb') as office_out:
        try:
            # load_key just inputs a password; you need to call decrypt to actually decrypt it.
            office_file.decrypt(office_out)
        except error:
            # Office 97~2003 Only: These files aren't supported yet.
            # If the password is CORRECT, msoffcrypto will through a generic 'error'
            return 'encrypted, but decryption not supported'
        except Exception:
            # Finally, msoffcrypto will throw a generic Exception on decrypt if the password is wrong
            return 'wrong password

    # just like pikepdf, you can't write over the file you're reading.
    # If you want to overwrite it, you must save it separately and then move it
    shutil.move(out_path, full_path)
```

The core steps to unlocking an office file are:

```python
with open(full_path, 'rb') as office_in:
    # Open the file
    office_file = msoffcrypto.OfficeFile(office_in)
    # Input the password
    office_file = msoffcrypto.load_key(password='mypassword')

    # open the output
    with open(out_path, 'wb') as office_out:
        # Run decrypt. This will write to the output file.
        office_file.decrypt(office_out)
```

But there are a _lot_ of things that can go wrong here, so the try-catch statements above are a must if you want any sense of stability.
