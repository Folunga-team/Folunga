
window.onload = function()
{
	canvas = document.getElementById("mycanvas");
	gl = canvas.getContext("webgl");

	const pixelRatio = window.devicePixelRatio || 1;
	canvas.width  = pixelRatio * canvas.clientWidth;
	canvas.height = pixelRatio * canvas.clientHeight;
	gl.viewport(0, 0, canvas.width, canvas.height);

	gl.clearColor(1, 1, 1, 0);
	gl.lineWidth(1.0);	
	
	
		
	var positions = [
		-1.0,  1.0, 0,
		 1.0,  1.0, 0,
		 1.0, -1.0, 0,
		-1.0,  1.0, 0,
		 1.0, -1.0, 0,
		-1.0, -1.0, 0
		];

	var colors = [
		1, 0, 0, 1,
		0, 1, 0, 1,
		0, 0, 1, 1,
		1, 0, 0, 1,
		0, 0, 1, 1,
		1, 0, 1, 1
		];
	
	var position_buffer = gl.createBuffer();

	gl.bindBuffer(
		gl.ARRAY_BUFFER, 
		position_buffer );

	gl.bufferData(
		gl.ARRAY_BUFFER,
		new Float32Array(positions),
		gl.STATIC_DRAW );

	var color_buffer = gl.createBuffer();

	gl.bindBuffer(
		gl.ARRAY_BUFFER, 
		color_buffer );

	gl.bufferData(
		gl.ARRAY_BUFFER,
		new Float32Array(colors),
		gl.STATIC_DRAW );
	
	
		
	const vs_source = document.getElementById('vertexShader').text;
	
	const vs = gl.createShader(gl.VERTEX_SHADER);
	gl.shaderSource(vs, vs_source);
	gl.compileShader(vs);

	if ( ! gl.getShaderParameter(vs, gl.COMPILE_STATUS) ) {
		alert( gl.getShaderInfoLog(vs) );
		gl.deleteShader(vs);
	}

	const fs_source = document.getElementById('fragmentShader').text;

	const fs = gl.createShader(gl.FRAGMENT_SHADER);
	gl.shaderSource(fs, fs_source);
	gl.compileShader(fs);

	if ( ! gl.getShaderParameter(fs, gl.COMPILE_STATUS) ) {
		alert( gl.getShaderInfoLog(fs) );
		gl.deleteShader(fs);
	}
	
	prog = gl.createProgram();
	gl.attachShader(prog, vs);
	gl.attachShader(prog, fs);
	gl.linkProgram(prog);

	if ( ! gl.getProgramParameter(prog, gl.LINK_STATUS) ) {
		alert( gl.getProgramInfoLog(prog) );
	}
	
	
	var m = gl.getUniformLocation(prog,'trans');

	var matrix = [
		1,0,0,0,
		0,1,0,0,
		0,0,1,0,
		0,0,0,1 ];

	gl.useProgram(prog);
	gl.uniformMatrix4fv( m, false, matrix );
	

	var p = gl.getAttribLocation(prog, 'pos');
	gl.bindBuffer(gl.ARRAY_BUFFER, position_buffer);
	gl.vertexAttribPointer(p, 3, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(p);

	var c = gl.getAttribLocation(prog, 'clr');
	gl.bindBuffer(gl.ARRAY_BUFFER, color_buffer);
	gl.vertexAttribPointer(c, 4, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(c);


	gl.clear( gl.COLOR_BUFFER_BIT );
	gl.useProgram( prog );
	gl.drawArrays( gl.TRIANGLES, 0, 6 );
}
