CHANGIA - ONLINE DONATION PLATFORM

So basically I’m building a donation website. You know how people share M-Pesa till numbers on WhatsApp when they’re fundraising? I want to make that more organized and automatic. Someone creates a campaign on the site, people donate through M-Pesa, and everything updates on its own. No more manually checking who sent what.

The Main Features
1. User Management
	•	Register and log in
	•	Two roles — Admin and Creator
	•	Password reset and change password
	•	Secure login using JWT tokens (basically a secure key you get when you log in)

2. Campaign Management
	•	Create a fundraising campaign with a title, description, target amount and deadline
	•	Edit, pause or close a campaign
	•	Track how much has been raised vs the goal

3. M-Pesa Payment Flow
	•	Donor enters their phone number and amount
	•	Our system calls Safaricom’s Daraja API
	•	Safaricom sends an STK push to the donor’s phone (that prompt asking for PIN)
	•	Donor enters PIN and pays
	•	Safaricom sends a callback to our system confirming payment
	•	Donation is automatically marked as successful
	•	We also handle cases where the callback comes twice (no duplicate donations)

4. 📊 Reports & Dashboard
	•	Creator sees: total raised, number of donors, successful vs failed payments
	•	Admin sees: everything across all campaigns and users

5. 📋 Logs & Audit Trail
	•	Every important action is recorded
	•	Who logged in, who created a campaign, when a donation came in
	•	Useful for debugging and monitoring



The Simple Flow of a Donation

  Donor opens a campaign
          ↓
  Clicks Donate → enters phone number + amount
          ↓
  Our system calls M-Pesa (Daraja API)
          ↓
  M-Pesa prompts donor's phone → donor enters PIN
          ↓
  Safaricom tells our system: "Payment successful"
          ↓
  Donation is recorded → campaign total updates
          ↓
  Creator sees it on their dashboard 

  

How the Database is Organized
Table             What it Stores
Users             Name, email, password, role
Campaigns         Title, description, goal amount, status
Donations         Amount, donor phone, payment status, campaign
Logs              Who did what and when



Current Status
This project is currently being built step by step. Here’s the plan:
	•	Project planning and design
	•	Backend setup (Django + PostgreSQL)
	•	User authentication (register, login, roles)
	•	Campaign management APIs
	•	M-Pesa Daraja integration
	•	Frontend (React)
	•	Reports and dashboard
	•	Logs and audit trail
