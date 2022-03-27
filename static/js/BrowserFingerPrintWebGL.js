function webgl(){
var canvas, ctx, width = 256, height = 128;
canvas = document.body.appendChild(document.createElement("canvas"));
canvas.width = width,
canvas.height = height,

ctx = canvas.getContext("webgl2") || canvas.getContext("experimental-webgl2") || canvas.getContext("webgl") || canvas.getContext("experimental-webgl") || canvas.getContext("moz-webgl");

    try {
        var f = "attribute vec2 attrVertex;varying vec2 varyinTexCoordinate;uniform vec2 uniformOffset;void main(){varyinTexCoordinate=attrVertex+uniformOffset;gl_Position=vec4(attrVertex,0,1);}";
        var g = "precision mediump float;varying vec2 varyinTexCoordinate;void main() {gl_FragColor=vec4(varyinTexCoordinate,0,1);}";
        var h = ctx.createBuffer();

        ctx.bindBuffer(ctx.ARRAY_BUFFER, h);

        var i = new Float32Array([-.2, -.9, 0, .4, -.26, 0, 0, .7321, 0]);

        ctx.bufferData(ctx.ARRAY_BUFFER, i, ctx.STATIC_DRAW), h.itemSize = 3, h.numItems = 3;

        var j = ctx.createProgram();
        var k = ctx.createShader(ctx.VERTEX_SHADER);

        ctx.shaderSource(k, f);
        ctx.compileShader(k);

        var l = ctx.createShader(ctx.FRAGMENT_SHADER);

        ctx.shaderSource(l, g);
        ctx.compileShader(l);
        ctx.attachShader(j, k);
        ctx.attachShader(j, l);
        ctx.linkProgram(j);
        ctx.useProgram(j);

        j.vertexPosAttrib = ctx.getAttribLocation(j, "attrVertex");
        j.offsetUniform = ctx.getUniformLocation(j, "uniformOffset");

        ctx.enableVertexAttribArray(j.vertexPosArray);
        ctx.vertexAttribPointer(j.vertexPosAttrib, h.itemSize, ctx.FLOAT, !1, 0, 0);
        ctx.uniform2f(j.offsetUniform, 1, 1);
        ctx.drawArrays(ctx.TRIANGLE_STRIP, 0, h.numItems);

    }
    catch (e) {	}

    var m = "";

var n = new Uint8Array(width * height * 4);
ctx.readPixels(0, 0, width, height, ctx.RGBA, ctx.UNSIGNED_BYTE, n);
m = JSON.stringify(n).replace(/,?"[0-9]+":/g, "");

document.getElementById('id_fingerprint').value = sha256(m);

// var protocolDomain = document.getElementById('id_protocol_current_domain').getAttribute('data-protocol_current_domain');
// $.ajax({
//     url: protocolDomain,
//     headers: {
//         'Browser-Fignerprint-ID': sha256(m)
//     }
// });
}

var sha256 = (function(){

// Eratosthenes seive to find primes up to 311 for magic constants. This is why SHA256 is better than SHA1
var i = 1,
    j,
    K = [],
    H = [];

while(++i < 18){
    for(j = i * i; j < 312; j += i){
    K[j] = 1;
    }
}

function x(num, root){
    return (Math.pow(num, 1 / root) % 1) * 4294967296|0;
}

for(i = 1, j = 0; i < 313; ){
    if(!K[++i]){
    H[j] = x(i,2);
    K[j++] = x(i,3);
    }
}

function S (X, n) { return ( X >>> n ) | (X << (32 - n)); }

function SHA256(b){
    var HASH = H.slice(i = 0),
        s = unescape(encodeURI(b)), /* encode as utf8 */
        W = [],
        l = s.length,
        m = [],
        a, y, z;
    for(; i < l; ) m[i >> 2] |= (s.charCodeAt(i) & 0xff) << 8 * (3 - i++ % 4);

    l *= 8;

    m[l >> 5] |= 0x80 << (24 - l % 32);
    m[z = (l + 64 >> 5) | 15] = l;

    for(i = 0; i < z; i += 16){
    a = HASH.slice(j = 0, 8);

    for(; j < 64; a[4] += y){
        if(j < 16){
        W[j] = m[j + i];
        }else{
        W[j] =
            (S(y = W[j - 2], 17) ^ S(y, 19) ^ (y >>> 10)) +
            (W[j - 7]|0) +
            (S(y = W[j - 15], 7) ^ S(y, 18) ^ (y >>> 3)) +
            (W[j - 16]|0);
        }

        a.unshift(
        (
            y = (
            a.pop() +
            (S(b = a[4], 6) ^ S(b, 11) ^ S(b, 25)) +
            (((b & a[5]) ^ ((~b) & a[6])) + K[j])|0
            ) +
            (W[j++]|0)
        ) +
        (S(l = a[0], 2) ^ S(l, 13) ^ S(l, 22)) +
        ((l & a[1]) ^ (a[1] & a[2]) ^ (a[2] & l))
        );
    }

    for(j = 8; j--; ) HASH[j] = a[j] + HASH[j];
    }

    for(s = ''; j < 63; ) s += ((HASH[++j >> 3] >> 4 * (7 - j % 8)) & 15).toString(16);

    return s;
}

return SHA256;
})();

setTimeout(webgl, 1);