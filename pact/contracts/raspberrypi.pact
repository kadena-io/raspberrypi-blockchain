(define-keyset 'admin-keyset (read-keyset "admin-keyset"))

(module raspberrypi 'admin-keyset
 @doc "Read and Update temperature and humidity."

 (defschema temp-humidity
  @doc "One row table for temeperature and humidity"
  temperature:decimal
  humidity:decimal
  time:time
  keyset:keyset)

 (deftable temp-humidity-table:{temp-humidity})

 (defun update-temp-humidity ( temperature:decimal
                               humidity:decimal
                               time:time
                               keyset:string )
  @doc "updates temperature and humidity values for every 20 minutes"
  (enforce-keyset (read-keyset "admin-keyset"))
  (write temp-humidity-table "1"
         { "temperature": temperature
         , "humidity": humidity
         , "time" : time
         , "keyset": (read-keyset keyset)
         }))

 (defun read-temp-humidity ()
  @doc "Read only row from table and returns it."
  (with-read temp-humidity-table "1"
             { "temperature":=temperature
             , "humidity":=humidity
             , "time":=time
             } [temperature humidity time]))

 (defun logs()
  @doc "Gives all updates"
  (keylog temp-humidity-table "1" 0))
)

(create-table temp-humidity-table)
(insert temp-humidity-table "1"
        { "temperature": 25.1
        , "humidity": 70.5
        , "time" : (time "2016-07-23T13:30:45Z")
        , "keyset": (read-keyset "admin-keyset")
        })
