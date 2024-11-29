CREATE DATABASE justicia;
USE justicia;

CREATE TABLE users(
    id INT(11) NOT NULL PRIMARY KEY,
    telegram_name VARCHAR(20),
    full_name VARCHAR(50),
    names VARCHAR(30),
    last_names VARCHAR(30),
    phone_number varchar(20),
    ci INT(11),
    school VARCHAR(30),
    birthdate date,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    day_week VARCHAR(10) NOT NULL,
    gender VARCHAR(1),
    rol VARCHAR(20)
);

CREATE TABLE user_properties(
    user_id INT(11) NOT NULL,
    balance FLOAT(20) DEFAULT 0 NOT NULL,
    tokens_available INT(10) DEFAULT 10 NOT NULL,
    unlimited_tokens INT(10) DEFAULT 0 NOT NULL,
    last_connection date,
    user_state INT(1) DEFAULT 1 NOT NULL,
    state_functions VARCHAR(20) DEFAULT "normal" NOT NULL,
    user_password VARCHAR(100),
    CONSTRAINT fk_user_properties_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE social_networks(
    user_id INT(11) NOT NULL,
    instagram_link VARCHAR(100),
    facebook_link VARCHAR(100),
    x_link VARCHAR(100),
    whatsapp_link VARCHAR(100),
    telegram_link VARCHAR(100),
    tik_tok_link VARCHAR(100),
    email VARCHAR(50),
    CONSTRAINT fk_social_networks_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE messages (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    chat_id INT(11) NOT NULL,
    user_id INT(11) NOT NULL,
    content VARCHAR(1000) NOT NULL,
    sent_date DATE NOT NULL DEFAULT CURDATE(),
    sent_time TIME NOT NULL DEFAULT CURTIME(),
    day_week VARCHAR(10) NOT NULL,
    message_type VARCHAR(10) NOT NULL,
    importance INT(5),
    CONSTRAINT fk_messages_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE documents (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    document_name VARCHAR(100),
    sent_date DATE NOT NULL DEFAULT CURDATE(),
    sent_time TIME NOT NULL DEFAULT CURTIME(),
    day_week VARCHAR(10) NOT NULL,
    path_doc  VARCHAR(100) NOT NULL,
    CONSTRAINT fk_documents_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE events (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    event_name VARCHAR(50),
    event_date DATE NOT NULL,
    day_week VARCHAR(10) NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    notification_to VARCHAR(20),
    location_event VARCHAR(100),
    CONSTRAINT fk_events_users FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE faculties (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(50),
    information VARCHAR(50)
);

CREATE TABLE schools (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    school_name VARCHAR(50),
    faculty INT (11),
    CONSTRAINT fk_school_faculty FOREIGN KEY (id) REFERENCES faculties(id)
);

CREATE TABLE coordinations (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    faculty_id INT(11) NOT NULL,
    school_id INT(11) NOT NULL,
    manager_id INT(11) NOT NULL,
    document_id INT(11) NOT NULL,
    CONSTRAINT fk_coordinations_faculty_id FOREIGN KEY (faculty_id) REFERENCES faculties(id),
    CONSTRAINT fk_coordinations_school_id FOREIGN KEY (school_id) REFERENCES schools(id),
    CONSTRAINT fk_coordinations_manager_id FOREIGN KEY (manager_id) REFERENCES users(id),
    CONSTRAINT fk_coordinations_information FOREIGN KEY (document_id) REFERENCES documents(id)
);

INSERT INTO `users` (`id`, `telegram_name`, `full_name`, `names`, `last_names`,`phone_number`, `ci`, `school`, `birthdate`, `day_week`, `gender`, `rol`) VALUES
(1, '@Justic-IA', 'Justicia', NULL, NULL, NULL, NULL, NULL, '2024-07-07', 'Miércoles', 'w', 'Master');