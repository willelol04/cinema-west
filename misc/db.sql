use cinema;

drop table movie;
create table movie(id int not null, title varchar(255) not null, overview varchar(1000) not null, poster_path varchar(255), release_date DATE not null, language varchar(50) not null, primary key(id))

insert into movie(id, title, overview, release_date, language) values(1322, "Movie 3", "Lorem ipsum dolor sit amet, ipsum dolor sit amet, ipsum dolor sit amet.", '2024-01-01', "en");

drop table user;
create table user(id int AUTO_INCREMENT not null, f_name varchar(50) not null, l_name varchar(50) not null, email varchar(100) not null, password varchar(30) not null, is_admin bool default false not null, primary key(id), unique(email));

drop table theatre;
create table theatre(id int auto_increment not null, name varchar(30) not null, primary key(id));
insert into theatre(name) values("Alpha");
insert into theatre(name) values("Beta");

drop table seat;
create table seat(id int AUTO_INCREMENT not null, number int not null, theatre_id int not null, primary key(id), Foreign Key (theatre_id) REFERENCES theatre(id), unique key(theatre_id, number))

drop table screening;
create table screening(id int AUTO_INCREMENT NOT NULL, movie_id int not null, theatre_id int not null, start_time datetime not null, is_cancelled bool default false not null, primary key(id), Foreign Key (theatre_id) REFERENCES theatre(id), Foreign Key (movie_id) REFERENCES movie(id), unique (theatre_id, start_time));

drop table ticket;
create table ticket(id int AUTO_INCREMENT not null, user_id int not null, screening_id int not null, seat_id int not null, created_at datetime default NOW() not null, is_cancelled bool default false not null, primary key(id), foreign key (user_id) references user(id), foreign key (screening_id) references screening(id), foreign key(seat_id) references seat(id), unique(screening_id, seat_id));