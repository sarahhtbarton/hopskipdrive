# **Rides**
----
  Returns json data about rides available to a driver. Data includes score, earnings, ride start address, and ride end address, and is ordered descending by score.

## **URL**

  /rides

## **Method:**
  
  `GET`
  
## **URL Params**

   **Required:**
 
   None

   **Optional:**
 
   None

## **Data Params**

  None

## **Authentication:**

  **Required**

  Need to call /rides with an authenticated session -- driver must first login on homepage.

## **Success Response:**

  * **Code:** 200 <br />
    **Sample Response:** `{
  "36": {
    "earnings": 15.0, 
    "start_address": "ChIJOR1geCGHhYARQ484akGas0M", 
    "end_address": "ChIJVVVVVYx3j4ARP-3NGldc8qQ"
  }, 
  "35": {
    "earnings": 14.15, 
    "start_address": "ChIJQ-U7wYqAhYAReKjwcBt6SGU", 
    "end_address": "ChIJkeRXUeaFj4ARcJTwcuK8jaY"
  }, 
  "29": {
    "earnings": 10.1, 
    "start_address": "ChIJHRGLQeuAhYARm3G81gyW59Y", 
    "end_address": "ChIJ3ygHDwGFhYARNd_3AnMlZsM"
  }, 
  "19": {
    "earnings": 5.75, 
    "start_address": "ChIJPwvLyD5-j4AR2fM8C0bbVC8", 
    "end_address": "ChIJo7HdhWKAhYARp5lDOzOnnK0"
  }, 
  "17": {
    "earnings": 7.65, 
    "start_address": "ChIJx6E1sUuHj4ARCB_Ub0Lb8fI", 
    "end_address": "ChIJRzfD3i98hYAR7TeEIqsZjys"
  }, 
  "14": {
    "earnings": 5.1, 
    "start_address": "ChIJKY2A05J9hYAR3ftxkR1ZTho", 
    "end_address": "ChIJcQMtojp8hYARg3TZouAOzFE"
  }, 
  "7": {
    "earnings": 3.0, 
    "start_address": "ChIJ64OBgvGKj4AR3jMzcn9tdWI", 
    "end_address": "ChIJ22W3TsJhhYARGF5WvDq2FhA"
  }
}`
 
## **Error Response:**

  * **Code:** 500 Internal Server Error -- Key Error: no authenticated session <br />
    **Content:** `KeyError: 'driver_id'`
