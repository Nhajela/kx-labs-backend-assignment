from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .views import VibeCheck, MainCharacterEnergy, CreativeClutter, WildIdea, TeaSpiller
from .serializers import (
    VibeCheckSerializer, MainCharacterEnergySerializer,
    CreativeClutterSerializer, WildIdeaSerializer, TeaSpillerSerializer
)
from .permissions import VibeCheckPermission, MainCharacterPermission, ChaoticPermission
from .filters import VibeCheckFilter, MainCharacterEnergyFilter, CreativeClutterFilter, TeaSpillerFilter

class VibeCheckViewSet(viewsets.ModelViewSet):
    queryset = VibeCheck.objects.all()
    serializer_class = VibeCheckSerializer
    permission_classes = [VibeCheckPermission]
    filterset_class = VibeCheckFilter
    
    @action(detail=False, methods=['get'])
    def current_vibe(self, request):
        latest = self.get_queryset().order_by('-created_at').first()
        if latest:
            serializer = self.get_serializer(latest)
            return Response(serializer.data)
        return Response({'vibe_status': 'mixed_vibes'})
    
    @action(detail=True, methods=['post'])
    def amplify(self, request, pk=None):
        vibe = self.get_object()
        vibe.energy_level = min(100, vibe.energy_level + 10)
        vibe.save()
        return Response({'message': 'Energy amplified!', 'new_level': vibe.energy_level})

class MainCharacterEnergyViewSet(viewsets.ModelViewSet):
    queryset = MainCharacterEnergy.objects.all()
    serializer_class = MainCharacterEnergySerializer
    permission_classes = [MainCharacterPermission]
    filterset_class = MainCharacterEnergyFilter
    
    @action(detail=True, methods=['post'])
    def stack_vibes(self, request, pk=None):
        energy = self.get_object()
        amount = request.data.get('amount', 10)
        energy.stack_vibes(amount)
        return Response({'message': f'Stacked {amount} vibes!', 'current_energy': energy.current_energy})
    
    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        top_energies = self.get_queryset().order_by('-current_energy')[:10]
        serializer = self.get_serializer(top_energies, many=True)
        return Response(serializer.data)

class CreativeClutterViewSet(viewsets.ModelViewSet):
    queryset = CreativeClutter.objects.all()
    serializer_class = CreativeClutterSerializer
    filterset_class = CreativeClutterFilter
    
    @action(detail=True, methods=['post'])
    def fix_mess(self, request, pk=None):
        clutter = self.get_object()
        clutter.fix_this_mess_please()
        return Response({'message': 'Mess fixed!', 'chaos_level': clutter.chaos_level})
    
    @action(detail=False, methods=['get'])
    def chaos_report(self, request):
        total_chaos = sum(c.chaos_level for c in self.get_queryset())
        return Response({
            'total_chaos': total_chaos,
            'average_chaos': total_chaos / self.get_queryset().count() if self.get_queryset().count() > 0 else 0,
            'recommendation': 'touch_grass' if total_chaos > 500 else 'good_vibes'
        })