
(in-package :cl-user)



(defun asdf-setpath ()
  (let* ((here-directory
          (concatenate 'string
                       (read-line (sb-ext:process-output
                                   (sb-ext:run-program "/bin/pwd" '() :output :stream)))
                       "/"))
         (here-path
          (concatenate 'string here-directory "redsight.asd")))

    (setq asdf:*central-registry*
          (cons (pathname here-directory)
                (remove here-directory *central-registry* :test #'pathname-match-p)))
    (load (pathname here-path))))
