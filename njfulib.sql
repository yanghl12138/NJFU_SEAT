create table users
(
id char(10) primary key,
pwd varchar(45) not null,
email varchar(45)
);

create table record
(
uid int auto_increment,
id char(10) not null,
seats varchar(512) not null,
start varchar(10) not null,
end varchar(10) not null,
primary key(uid, id),
constraint fk_id foreign key record(id) 
references users(id) on delete cascade
);

create view info as
select users.id, email, seats, start, end from users inner join record on users.id = record.id;