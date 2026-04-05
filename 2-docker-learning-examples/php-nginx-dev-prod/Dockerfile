FROM php:8.2-fpm-alpine AS base

WORKDIR /var/www/html

RUN apk add --no-cache bash \
    && docker-php-ext-install pdo pdo_mysql

COPY src/ /var/www/html/

RUN mkdir -p /opt/bootstrap/public /opt/bootstrap/storage \
    && cp -R /var/www/html/public/. /opt/bootstrap/public/ \
    && if [ -d /var/www/html/storage ]; then cp -R /var/www/html/storage/. /opt/bootstrap/storage/; fi \
    && chown -R www-data:www-data /var/www/html /opt/bootstrap

FROM base AS development

RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"

CMD ["php-fpm"]

FROM base AS production

RUN apk add --no-cache rsync \
    && mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

COPY docker/entrypoint-prod.sh /usr/local/bin/entrypoint-prod.sh

RUN chmod +x /usr/local/bin/entrypoint-prod.sh

ENTRYPOINT ["entrypoint-prod.sh"]
CMD ["php-fpm"]
