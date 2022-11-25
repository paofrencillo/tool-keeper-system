var scanner = new Instascan.Scanner({ video: document.getElementById('preview'), scanPeriod: 5, mirror: false });
Instascan.Camera.getCameras().then(function (cameras){
    if(cameras.length>0){
        scanner.start(cameras[0]);
        $('[name="options"]').on('change',function(){
            if($(this).val()==1){
                if(cameras[0]!=""){
                    scanner.start(cameras[0]);
                }else{
                    alert('No Camera Found!');
                }
            }
        });
    }else{
        console.error('No cameras found.');
        alert('No cameras found.');
    }
}).catch(function(e){
    console.error(e);
    alert(e);
});
scanner.addListener('scan', function(content) {
    document.getElementById('text').value = content;
});