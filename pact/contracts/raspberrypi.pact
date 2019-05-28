(define-keyset 'admin-keyset (read-keyset "admin-keyset"))

(module raspberrypi 'admin-keyset
 @doc "Read and Update temperature, humidity and gps."

 (defschema temp-humidity-gps
  @doc "One row table for temeperature, humidity and gps"
  temperature:decimal
  humidity:decimal
  latitude:decimal
  longitude:decimal
  time:time
  keyset:keyset)

 (deftable temp-humidity-gps-table:{temp-humidity-gps})

 (defun update-temp-humidity-gps ( temperature:decimal
                                   humidity:decimal
                                   latitude:decimal
                                   longitude:decimal
                                   time:time
                                   keyset:string )
  @doc "updates temperature, humidity and gps values for every 20 minutes"
  (enforce-keyset (read-keyset "admin-keyset"))
  (write temp-humidity-gps-table "1"
         { "temperature": temperature
         , "humidity": humidity
         , "latitude": latitude
         , "longitude": longitude
         , "time" : time
         , "keyset": (read-keyset keyset)
         }))

 (defun read-temp-humidity-gps ()
  @doc "Read only row from table and returns it."
  (with-read temp-humidity-gps-table "1"
             { "temperature":=temperature
             , "humidity":=humidity
             , "latitude":= latitude
             , "longitude":= longitude
             , "time":=time
             } [temperature humidity latitude longitude time]))

 (defun logs()
  @doc "Gives all updates"
  (keylog temp-humidity-gps-table "1" 0))
)

(create-table temp-humidity-gps-table)

(insert temp-humidity-gps-table "1"
        { "temperature": 25.1
        , "humidity": 70.5
        , "latitude": 10.123
        , "longitude": 32.55556
        , "time" : (time "2016-07-23T13:30:45Z")
        , "keyset": (read-keyset "admin-keyset")
        })
