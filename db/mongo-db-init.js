db.createUser({
  user: "adminbv",
  pwd: "boavizinhanca2020",
  roles: [
    {
      role: "readWrite",
      db: "admin",
    },
  ],
  mechanisms: ["SCRAM-SHA-1"],
});

// mongo --port 27017 - u "adminbv" - p ".boavizinhanca2020" --authenticationDatabase "local"
