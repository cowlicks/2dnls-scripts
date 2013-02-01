function plotnlsdata
    
    z = load('out/z'); 
    x = load('out/x'); 
    y = load('out/y'); 

    nz = length(z); 

    fig = figure; 

    max_a2 = zeros(1,nz); 

    for n = 1 : nz

      ar_file = ['out/ar.' sprintf('%04g',n-1)];
      ai_file = ['out/ai.' sprintf('%04g',n-1)];  
      if ( exist(ar_file) & exist(ai_file) )
        ar = load(ar_file); 
        ai = load(ai_file); 
      else
        disp('ERROR: unable to find file');
        break; 
      end
      
      a = ar + ai*i; 
      a2 = a.*conj(a); 
      
      max_a2(n) = max(max(a2)); 
      
      pcolor(x,y,a2); shading interp; colorbar; 
      xlabel('x/w_0'); 
      ylabel('y/w_0'); 
      titletext = ['|a|^2/a_0^2 at z/z_R = ' sprintf('%g',z(n))];
      title(titletext); 
      
      out_file = ['out.' sprintf('%04g',n-1) '.png']; 
      print(fig,'-dpng','-r300',out_file); 

    end
endfunction

plotnlsdata
