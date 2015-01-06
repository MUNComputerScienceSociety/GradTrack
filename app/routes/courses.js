var express = require('express');
var router = express.Router();

var select = {
  allDepartments: 'select * from departments',
  courseByID: 'select * from courses where id=? limit 1'
};

var insert = {
};

function success(data) {
  return {error: null, data: data};
}

function failure(error) {
  return {error: error, data: null};
};

function courseFromRow(row) {
  return {  
    id: row[0],
    departmentID: row[1],
    identifier: row[2],
    title: row[3],
    number: row[4],
    description: row[5]
  };
}

module.exports = function (db) {
  var getAllDepartments = function (req, res) {
    db.all(select.allDepartments, function (err, rows) {
      if (err) {
        res.send(failure(err));
      } else {
        res.send(success(rows));
      }
    });
  };
  
  // The course index page gets a list of departments to search by department.
  router.get('/', getAllDepartments);
  router.get('/departments', getAllDepartments);

  // Get a single course by its id.
  router.get('/:id', function (req, res) {
    db.get(select.courseByID, function (err, row) {
      if (err) {
        res.send(failure(err));
      } else {
        res.send(success(courseFromRow(row)));
      }
    });
  });

  return router;
};
