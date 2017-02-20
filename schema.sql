drop table if exists login_credentials;
create table login_credentials (
  username char(32) primary key,
  password char(32) not null
);

insert into login_credentials (username, password) values ('roby','roby');
insert into login_credentials (username, password) values ('reception','health+');
insert into login_credentials (username, password) values ('sujay','sujay');
insert into login_credentials (username, password) values ('atharva','atharva');
insert into login_credentials (username, password) values ('abhijeet','abhijeet');
insert into login_credentials (username, password) values ('pranav','pranav');
insert into login_credentials (username, password) values ('shubham','shubham');
insert into login_credentials (username, password) values ('swapnil','swapnil');
insert into login_credentials (username, password) values ('abhay','abhay');


drop table if exists details;
create table details (
  username char(32) primary key,
  patient_name char(32) default "Not Registered", 
  patient_age char(32) default "Not Registered",
  patient_sex char(32) default "Not Registered",
  patient_blood_group char(32) default "Not Registered",
  patient_weight char(32) default "Not Registered",
  patient_contact char(32) default "Not Registered"
);

insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('roby','Onkar Singh', '21', 'M' , 'O+' , '76' , '9816926947');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('sujay','Sujay Khandagale', '19', 'M' , 'O-' , '80' , '8888826249');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('atharva','Atharva Nijasure', '19', 'M' , 'A+' , '76' , '9732448232');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('sahil','Sahil Singla', '19', 'M' , 'B+' , '72' , '9816926947');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('abhijeet','Abhijeet Bajaj', '19', 'M' , 'B+' , '62' , '9816929842');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('pranav','Pranav Kulkarni', '18', 'M' , 'AB+' , '88' , '7424582843');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('abhay','Abhay Singh Chauhan', '19', 'M' , 'B-' , '50' , '8989016289');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('swapnil','Swapnil Sharma', '17', 'M' , 'A-' , '85' , '9816924324');
insert into details (username, patient_name, patient_age, patient_sex, patient_blood_group, patient_weight, patient_contact) values ('Shubham','Shubham Patil', '20', 'M' , 'B+' , '72' , '9404146226');

drop table if exists appointments;
create table appointments (
	username char(32) not null,
	name char(32) not null,
	email char(32) not null,
	booking_date char(32) not null,
	department char(32) not null,
  status char(32) default 'false',
  primary key(username, booking_date)
);

insert into appointments (username, name, email, booking_date, department, status) values ('roby','Onkar','roby','11/23/2016','Health Care','true');
insert into appointments (username, name, email, booking_date, department, status) values ('roby','Onkar','roby','11/24/2016','Body Checkup','true');
insert into appointments (username, name, email, booking_date, department, status) values ('atharva','Atharva','atharva','11/25/2016','Out Patient','true');
insert into appointments (username, name, email, booking_date, department, status) values ('sujay','Sujay Khandagale','sujay','11/20/2016','Surgery','false');
insert into appointments (username, name, email, booking_date, department, status) values ('sujay','Sujay Khandagale','sujay','11/22/2016','Out Patient','false');
insert into appointments (username, name, email, booking_date, department, status) values ('sujay','Sujay Khandagale','sujay','11/24/2016','Body Checkup','false');
insert into appointments (username, name, email, booking_date, department, status) values ('sahil','Sahil Singla','sahil','11/20/2016','Body Checkup','false');
insert into appointments (username, name, email, booking_date, department, status) values ('abhay','Abhay Singh Chauhan','abhay','11/20/2016','Health Care','true');
insert into appointments (username, name, email, booking_date, department, status) values ('shubham','Shubham Patil','shubham','9/16/2016','Surgery','false');
insert into appointments (username, name, email, booking_date, department, status) values ('pranav','Pranav Kulkarni','pranav','10/20/2016','Out Patient','true');




drop table if exists records;
create table records(
  username char(32) not null,
  visit_date char(32) not null,
  prescription char(255) not null,
  primary key(username, visit_date)
);

insert into records (username, visit_date, prescription) values ('roby','11/23/2016','Cold Cough and Fever');
insert into records (username, visit_date, prescription) values ('roby','11/24/2016','Body Checkup normal.');
insert into records (username, visit_date, prescription) values ('atharva','11/25/2016','Severe abdominal pain since a week. Treated for mild appendicitis. Medicines prescribed as per need.');
insert into records (username, visit_date, prescription) values ('abhay','11/20/2016','Severe abdominal pain since a week. Treated for mild appendicitis. Medicines prescribed as per need.');
insert into records (username, visit_date, prescription) values ('pranav','10/20/2016','Severe abdominal pain since a week. Treated for mild appendicitis. Medicines prescribed as per need.');





