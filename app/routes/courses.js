var express = require('express');
var router = express.Router();

var select = {
  allDepartments: 'select * from departments',
  courseByID: 'select * from courses where id=?'
};

var insert = {
};

function success(data) {
  return {error: null, data: data};
}

function failure(err) {
  return {error: err, data: null};
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
    var id = parseInt(req.params.id);
    if (isNaN(id)) {
      res.send(failure(new Error('Invalid ID type supplied.')));
    } else {
      var statement = db.prepare(select.courseByID);
      statement.get(id, function (err, row) {
        if (err) {
          res.send(failure(err));
        } else if (typeof row === 'undefined' || !row) {
          res.send(failure(new Error('No course with identifier ' + id + ' was found.')));
        } else {
          res.send(success(row));
        }
      });
    }
  });

  return router;
};
