file.put:
  - hosts: all
  - source: file_source/httpd.conf
  - name: /data/www/httpd.conf
