# Loans_api

## Use case
A Lenme borrower would like to borrow $5,000.00 on paying them back in 6 months. One of the Lenme investors has offered him a 15% Annual Interest Rate. A $3.00 Lenme fee will be added to the total loan amount to be paid by the investor.  

## Requirements
You are required to develop a Django REST project to be able to build the following flow through its
APIs;
 
1. The borrower creates a loan request including the above loan amount and loan period 
2. The investor will submit an offer for the borrower’s loan request with the above interest rate
3. The borrower will accept the offer
4. Check if the investor has sufficient balance in their account before they fund the loan
5. The loan will be funded successfully and the loan status will be Funded
6. The loan payments will be created with the monthly amount to be paid and its due date
7. Once all the payments are successfully paid to the investor, the loan status will be Completed

## Future work
1- Handling authendication.
2- Managing payment jobs.
