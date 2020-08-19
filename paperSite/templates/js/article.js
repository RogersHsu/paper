function getArticle(articleGroup, postId) {
    return new Promise(function (resolve, reject) {
        jQuery.ajax({
            type: "GET",
            url: jQuery('meta[name="url"]').attr("content") + "/api/article/generic/" + articleGroup + "/get/" + postId,
            headers: {
                'X-CSRF-Token': jQuery('meta[name="X-CSRF-Token"]').attr("content")
            },
            success: resolve,
            error: reject
        });
    });
}

function getAllArticle(articleGroup) {
    return new Promise(function (resolve, reject) {
        jQuery.ajax({
            type: "GET",
            url: jQuery('meta[name="url"]').attr("content") + "/api/article/generic/" + articleGroup + "/get",
            headers: {
                'X-CSRF-Token': jQuery('meta[name="X-CSRF-Token"]').attr("content")
            },
            success: resolve,
            error: reject
        });
    });
}

function submitArticle(articleGroup, title, content) {
    return new Promise(function (resolve, reject) {
        jQuery.ajax({
            type: "POST",
            url: jQuery('meta[name="url"]').attr("content") + "/api/backstage/article/generic/" + articleGroup + "/post",
            headers: {
                'X-CSRF-Token': jQuery('meta[name="X-CSRF-Token"]').attr("content")
            },
            data: JSON.stringify({
                "title": title,
                "content": content
            }),
            success: function (data) {
                if (data.success) {
                    resolve(data);
                } else {
                    reject(data);
                }
            },
            error: reject
        });
    });
}

function updateArticle(articleGroup, postId, title, content, order) {
    return new Promise(function (resolve, reject) {
        jQuery.ajax({
            type: "POST",
            url: jQuery('meta[name="url"]').attr("content") + "/api/backstage/article/generic/" + articleGroup + "/patch/" + postId,
            headers: {
                'X-CSRF-Token': jQuery('meta[name="X-CSRF-Token"]').attr("content")
            },
            data: JSON.stringify({
                "title": title,
                "content": content,
                "order": order
            }),
            success: function (data) {
                if (data.success) {
                    resolve(data);
                } else {
                    reject(data);
                }
            },
            error: reject
        });
    });
}

function deleteArticle(articleGroup, postId) {
    return new Promise(function (resolve, reject) {
        jQuery.ajax({
            type: "POST",
            url: jQuery('meta[name="url"]').attr("content") + "/api/backstage/article/generic/" + articleGroup + "/delete/" + postId,
            headers: {
                'X-CSRF-Token': jQuery('meta[name="X-CSRF-Token"]').attr("content")
            },
            success: function (data) {
                if (data.success) {
                    resolve(data);
                } else {
                    reject(data);
                }
            },
            error: reject
        });
    });
}
