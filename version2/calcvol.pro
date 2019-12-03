; calcsurf.pro
; goes through missing_volume which is the result of the missing surface
; minus the original dem, with a mask applied so that we are looking
; at the missing material only

pro calcvol
ns = 2765
nl = 2910
pix_area = 463. * 463

voldat = dblarr(ns, nl)
openr,1,'version2/outrays_fill_1p5deg'
readu,1,voldat
close,/all

dem = intarr(ns, nl)
openr,1,'OlyMons2'
readu,1,dem
close,/all
sub = fltarr(ns,nl) -9999.
w = where (voldat gt -9999)
sub(w) =  voldat(w) - dem(w)
newsub = sub
nvals = where (sub lt 0)
newsub(nvals)=-9999 
npix = where (newsub gt 0)
tot_area = n_elements (npix) * pix_area
tot_vol = total(newsub(npix)) * pix_area
print, "area is : ", tot_area
print, "volume is : ", tot_vol 
stop
end

