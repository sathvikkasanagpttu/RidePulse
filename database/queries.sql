-- RidePulse analytics reference queries

-- Total rides
SELECT COUNT(*) AS total_rides FROM trips;

-- Unique starting locations
SELECT COUNT(DISTINCT start) AS total_locations FROM trips;

-- Average trip distance
SELECT ROUND(AVG(miles)::numeric, 2) AS avg_miles FROM trips;

-- Average trip duration
SELECT ROUND(AVG(duration_minutes)::numeric, 2) AS avg_duration FROM trips;

-- Hourly demand
SELECT hour_of_day, COUNT(*) AS ride_count
FROM trips GROUP BY hour_of_day ORDER BY hour_of_day;

-- Day-of-week demand
SELECT day_of_week, day_of_week_name, COUNT(*) AS ride_count
FROM trips GROUP BY day_of_week, day_of_week_name ORDER BY day_of_week;

-- Top starting locations
SELECT start, COUNT(*) AS ride_count
FROM trips GROUP BY start ORDER BY ride_count DESC LIMIT 10;

-- Monthly demand
SELECT month, COUNT(*) AS ride_count
FROM trips GROUP BY month ORDER BY month;

-- Category mix
SELECT category, COUNT(*) AS ride_count
FROM trips GROUP BY category ORDER BY ride_count DESC;

-- Purpose mix
SELECT purpose, COUNT(*) AS ride_count
FROM trips WHERE purpose IS NOT NULL
GROUP BY purpose ORDER BY ride_count DESC;

-- Top routes
SELECT start, "end", COUNT(*) AS ride_count
FROM trips GROUP BY start, "end"
ORDER BY ride_count DESC LIMIT 10;

-- Peak vs non-peak
SELECT is_peak_hr, COUNT(*) AS ride_count
FROM trips GROUP BY is_peak_hr ORDER BY is_peak_hr DESC;

-- Weekend vs weekday
SELECT is_weekend, COUNT(*) AS ride_count
FROM trips GROUP BY is_weekend;
