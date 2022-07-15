# Capstone

This is a capstone project for Optum Network Security & Automation.

For this project, I was thinking what would be a good way to demonstrate the integrity of the file being
shared between co-workers or peers in general. Additionally, in order to protect or at least to help narrow
down where the shared file could have been leaked from, if leaked, what would be a way to track it down
with record. 

Throughout the coding, there were multiple challenges: 
(1) The watermarker pdf was incorrectly merging with the pdf version of the requested file; requested page 
1 + watermarker + requested page 2 + watermarker + etc.
This problem was solved with googling the subject matter more and testing out different library functions.

(2) Once the watermarker page and the requested doc was merged, there were issues with md5sums on the header
of the page being cutout; only the second checksum would be visible. Although this required a further 
research, no relevant forums were found. Instead, this just required playing around with the code until I was
able to get the result that I wanted.

(3) There was an issue with send_email function, where I could not login even with the correct credentials.
I was unable to find the solution. However, I consulted a co-worker, who had the same issue and found out
that I had to enable Google's 3rd party access and grab the 3rd party app password provided by Google.
