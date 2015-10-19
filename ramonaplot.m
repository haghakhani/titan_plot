clear all
xyh=read_in_zgrid('maxkerecord.-00001');

%xyh=max_grid;
dxdy=(xyh(2,1,1)-xyh(1,1,1))*(xyh(1,2,2)-xyh(1,1,2));
vol=sum(sum(xyh(:,:,3)))*dxdy;
minmaxh=[(vol^(1/3))/10000; max(max(xyh(:,:,3)))];

XYZ=read_in_zgrid('elevation.grid');
X=XYZ(:,:,1); Y=XYZ(:,:,2); Z=XYZ(:,:,3); clear XYZ;

% xi=X(1:10,1)
% yi=Y(1:10,1)
% zi=Z(1:10,1)


xminmax=minmax(xyh(:,1,1)');
yminmax=minmax(xyh(1,:,2));
iX=find((X(:,1)>=xminmax(1))&(X(:,1)<=xminmax(2)));
iY=find((Y(1,:)>=yminmax(1))&(Y(1,:)<=yminmax(2)));
X=X(iX,iY);
Y=Y(iX,iY);
Z=Z(iX,iY);
Nx=size(X,1);
Ny=size(X,2);

H=interp2(xyh(:,:,1)',xyh(:,:,2)',xyh(:,:,3)',X,Y,'linear');
iHzero=find(H<minmaxh(1));
H(iHzero)=0.01;

%might want to comment out the next line
minmaxh=10.0.^[floor(log10(minmaxh(1))) ceil(log10(minmaxh(2)))];

Nquads=(Nx-1)*(Ny-1);
iX=shiftdim([1:Nx-1]'*ones(1,Ny-1),-1);
iY=shiftdim(ones(Nx-1,1)*[1:Ny-1],-1);
quads=zeros(4,Nx-1,Ny-1);
quads(1,:,:)=(iY-1)*Nx+iX;
quads(2,:,:)=(iY-1)*Nx+iX+1;
quads(3,:,:)=(iY-0)*Nx+iX+1;
quads(4,:,:)=(iY-0)*Nx+iX;
quads=reshape(quads,[4 Nquads]);    
       
cmap=colormap;
cmaplength=size(cmap,1);
icolor=round((log10(H)-log10(minmaxh(1)))/diff(log10(minmaxh))*cmaplength);
icolor(find(icolor>cmaplength))=cmaplength;
icolor(find(icolor<1))=1;
cvert=cmap(icolor,:);
cvert(iHzero,:)=1;

patch(X(quads),Y(quads),Z(quads),reshape(cvert(quads,:),4,Nquads,3));
shading flat;
axis image;
hcl=camlight;
caxis(minmaxh);
colorbar('vert','yscale','log');