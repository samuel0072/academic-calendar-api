CREATE TABLE `academic_calendars` (
  `id` integer PRIMARY KEY,
  `start_date` datetime,
  `end_date` datetime,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `campi` (
  `id` integer PRIMARY KEY,
  `name` text,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE TABLE `calendar_campus` (
  `academic_calendar_id` integer,
  `campus_id` integer
);

CREATE TABLE `event` (
  `id` integer PRIMARY KEY,
  `start_date` datetime,
  `end_date` datetime,
  `label` varchar(255),
  `description` text,
  `created_at` timestamp,
  `updated_at` timestamp,
  `academic_calendar_id` integer
);

ALTER TABLE `academic_calendars` ADD FOREIGN KEY (`id`) REFERENCES `calendar_campus` (`campus_id`);

ALTER TABLE `campi` ADD FOREIGN KEY (`id`) REFERENCES `calendar_campus` (`academic_calendar_id`);

ALTER TABLE `event` ADD FOREIGN KEY (`academic_calendar_id`) REFERENCES `academic_calendars` (`id`);
